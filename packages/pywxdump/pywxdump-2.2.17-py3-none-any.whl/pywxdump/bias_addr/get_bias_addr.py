# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         get_base_addr.py
# Description:  
# Author:       xaoyaoo
# Date:         2023/08/22
# -------------------------------------------------------------------------------
import argparse
import ctypes
import hashlib
import json
import multiprocessing
import os
import re
import sys

import psutil
from win32com.client import Dispatch
from pymem import Pymem
import pymem
import hmac

ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
void_p = ctypes.c_void_p
KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000


def validate_key(key, salt, first, mac_salt):
    byteKey = hashlib.pbkdf2_hmac("sha1", key, salt, DEFAULT_ITER, KEY_SIZE)
    mac_key = hashlib.pbkdf2_hmac("sha1", byteKey, mac_salt, 2, KEY_SIZE)
    hash_mac = hmac.new(mac_key, first[:-32], hashlib.sha1)
    hash_mac.update(b'\x01\x00\x00\x00')

    if hash_mac.digest() == first[-32:-12]:
        return True
    else:
        return False


def get_exe_bit(file_path):
    """
    获取 PE 文件的位数: 32 位或 64 位
    :param file_path:  PE 文件路径(可执行文件)
    :return: 如果遇到错误则返回 64
    """
    try:
        with open(file_path, 'rb') as f:
            dos_header = f.read(2)
            if dos_header != b'MZ':
                print('get exe bit error: Invalid PE file')
                return 64
            # Seek to the offset of the PE signature
            f.seek(60)
            pe_offset_bytes = f.read(4)
            pe_offset = int.from_bytes(pe_offset_bytes, byteorder='little')

            # Seek to the Machine field in the PE header
            f.seek(pe_offset + 4)
            machine_bytes = f.read(2)
            machine = int.from_bytes(machine_bytes, byteorder='little')

            if machine == 0x14c:
                return 32
            elif machine == 0x8664:
                return 64
            else:
                print('get exe bit error: Unknown architecture: %s' % hex(machine))
                return 64
    except IOError:
        print('get exe bit error: File not found or cannot be opened')
        return 64


def get_exe_version(file_path):
    """
    获取 PE 文件的版本号
    :param file_path:  PE 文件路径(可执行文件)
    :return: 如果遇到错误则返回
    """
    file_version = Dispatch("Scripting.FileSystemObject").GetFileVersion(file_path)
    return file_version


def find_all(c: bytes, string: bytes, base_addr=0):
    """
    查找字符串中所有子串的位置
    :param c: 子串 b'123'
    :param string: 字符串 b'123456789123'
    :return:
    """
    return [base_addr + m.start() for m in re.finditer(re.escape(c), string)]


class BiasAddr:
    def __init__(self, account, mobile, name, key, db_path):
        self.account = account.encode("utf-8")
        self.mobile = mobile.encode("utf-8")
        self.name = name.encode("utf-8")
        self.key = bytes.fromhex(key) if key else b""
        self.db_path = db_path if os.path.exists(db_path) else ""

        self.process_name = "WeChat.exe"
        self.module_name = "WeChatWin.dll"

        self.pm = None  # Pymem 对象
        self.is_WoW64 = None  # True: 32位进程运行在64位系统上 False: 64位进程运行在64位系统上
        self.process_handle = None  # 进程句柄
        self.pid = None  # 进程ID
        self.version = None  # 微信版本号
        self.process = None  # 进程对象
        self.exe_path = None  # 微信路径
        self.address_len = None  # 4 if self.bits == 32 else 8  # 4字节或8字节
        self.bits = 64 if sys.maxsize > 2 ** 32 else 32  # 系统：32位或64位

    def get_process_handle(self):
        try:
            self.pm = Pymem(self.process_name)
            self.pm.check_wow64()
            self.is_WoW64 = self.pm.is_WoW64
            self.process_handle = self.pm.process_handle
            self.pid = self.pm.process_id
            self.process = psutil.Process(self.pid)
            self.exe_path = self.process.exe()
            self.version = get_exe_version(self.exe_path)

            version_nums = list(map(int, self.version.split(".")))  # 将版本号拆分为数字列表
            if version_nums[0] <= 3 and version_nums[1] <= 9 and version_nums[2] <= 2:
                self.address_len = 4
            else:
                self.address_len = 8
            return True, ""
        except pymem.exception.ProcessNotFound:
            return False, "[-] WeChat No Run"

    def search_memory_value(self, value: bytes, module_name="WeChatWin.dll"):
        # 创建 Pymem 对象
        module = pymem.process.module_from_name(self.pm.process_handle, module_name)
        ret = self.pm.pattern_scan_module(value, module, return_multiple=True)
        ret = ret[-1] - module.lpBaseOfDll if len(ret) > 0 else 0
        return ret

    def get_key_bias1(self):
        try:
            byteLen = self.address_len  # 4 if self.bits == 32 else 8  # 4字节或8字节

            keyLenOffset = 0x8c if self.bits == 32 else 0xd0
            keyWindllOffset = 0x90 if self.bits == 32 else 0xd8

            module = pymem.process.module_from_name(self.process_handle, self.module_name)
            keyBytes = b'-----BEGIN PUBLIC KEY-----\n...'
            publicKeyList = pymem.pattern.pattern_scan_all(self.process_handle, keyBytes, return_multiple=True)

            keyaddrs = []
            for addr in publicKeyList:
                keyBytes = addr.to_bytes(byteLen, byteorder="little", signed=True)  # 低位在前
                may_addrs = pymem.pattern.pattern_scan_module(self.process_handle, module, keyBytes,
                                                              return_multiple=True)
                if may_addrs != 0 and len(may_addrs) > 0:
                    for addr in may_addrs:
                        keyLen = self.pm.read_uchar(addr - keyLenOffset)
                        if keyLen != 32:
                            continue
                        keyaddrs.append(addr - keyWindllOffset)

            return keyaddrs[-1] - module.lpBaseOfDll if len(keyaddrs) > 0 else 0
        except:
            return 0

    def search_key(self, key: bytes):
        key = re.escape(key)  # 转义特殊字符
        key_addr = self.pm.pattern_scan_all(key, return_multiple=False)
        key = key_addr.to_bytes(self.address_len, byteorder='little', signed=True)
        result = self.search_memory_value(key, self.module_name)
        return result

    def get_key_bias2(self, wx_db_path, account_bias=0):
        wx_db_path = os.path.join(wx_db_path, "Msg", "MicroMsg.db")
        if not os.path.exists(wx_db_path):
            return 0

        def get_maybe_key(mem_data):
            min_addr = 0xffffffffffffffffffffffff
            max_addr = 0
            for module1 in pm.list_modules():
                if module1.lpBaseOfDll < min_addr:
                    min_addr = module1.lpBaseOfDll
                if module1.lpBaseOfDll > max_addr:
                    max_addr = module1.lpBaseOfDll + module1.SizeOfImage

            maybe_key = []
            for i in range(0, len(mem_data), self.address_len):
                addr = mem_data[i:i + self.address_len]
                addr = int.from_bytes(addr, byteorder='little')
                # 去掉不可能的地址
                if min_addr < addr < max_addr:
                    key = read_key(addr)
                    if key == b"":
                        continue
                    maybe_key.append([key, i])
            return maybe_key

        def read_key(addr):
            key = ctypes.create_string_buffer(35)
            if ReadProcessMemory(pm.process_handle, void_p(addr - 1), key, 35, 0) == 0:
                return b""

            if b"\x00\x00" in key.raw[1:33]:
                return b""

            if b"\x00\x00" == key.raw[33:35] and b"\x90" == key.raw[0:1]:
                return key.raw[1:33]
            return b""

        def verify_key(keys, wx_db_path):
            with open(wx_db_path, "rb") as file:
                blist = file.read(5000)
            salt = blist[:16]
            first = blist[16:DEFAULT_PAGESIZE]
            mac_salt = bytes([(salt[i] ^ 58) for i in range(16)])

            with multiprocessing.Pool(processes=8) as pool:
                results = [pool.apply_async(validate_key, args=(key, salt, first, mac_salt)) for key, i in keys[-1::-1]]
                results = [p.get() for p in results]
                for i, result in enumerate(results[-1::-1]):
                    if result:
                        return keys[i]
                return b"", 0

        module_name = "WeChatWin.dll"
        pm = self.pm
        module = pymem.process.module_from_name(pm.process_handle, module_name)
        start_addr = module.lpBaseOfDll
        size = module.SizeOfImage

        if account_bias > 1:
            maybe_key = []
            for i in [0x24, 0x40]:
                addr = start_addr + account_bias - i
                mem_data = pm.read_bytes(addr, self.address_len)
                key = read_key(int.from_bytes(mem_data, byteorder='little'))
                if key != b"":
                    maybe_key.append([key, addr - start_addr])
            key, bais = verify_key(maybe_key, wx_db_path)
            if bais != 0:
                return bais

        mem_data = pm.read_bytes(start_addr, size)
        maybe_key = get_maybe_key(mem_data)
        key, bais = verify_key(maybe_key, wx_db_path)
        return bais

    def run(self, logging_path=False, version_list_path=None):
        if not self.get_process_handle()[0]:
            return None
        mobile_bias = self.search_memory_value(self.mobile, self.module_name)
        name_bias = self.search_memory_value(self.name, self.module_name)
        account_bias = self.search_memory_value(self.account, self.module_name)
        key_bias = 0
        key_bias = self.get_key_bias1()
        key_bias = self.search_key(self.key) if key_bias <= 0 and self.key else key_bias
        key_bias = self.get_key_bias2(self.db_path, account_bias) if key_bias <= 0 and self.db_path else key_bias

        rdata = {self.version: [name_bias, account_bias, mobile_bias, 0, key_bias]}
        if version_list_path and os.path.exists(version_list_path):
            with open(version_list_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data.update(rdata)
            with open(version_list_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        if os.path.exists(logging_path) and isinstance(logging_path, str):
            with open(logging_path, "a", encoding="utf-8") as f:
                f.write("{版本号:昵称,账号,手机号,邮箱,KEY}" + "\n")
                f.write(str(rdata) + "\n")
        elif logging_path:
            print("{版本号:昵称,账号,手机号,邮箱,KEY}")
            print(rdata)
        return rdata


# class BiasAddr:
#     def __init__(self, account, mobile, name, key, db_path):
#         self.account = account.encode("utf-8")
#         self.mobile = mobile.encode("utf-8")
#         self.name = name.encode("utf-8")
#         self.key = bytes.fromhex(key) if key else b""
#         self.db_path = db_path if db_path else ""
#
#         self.process_name = "WeChat.exe"
#         self.module_name = "WeChatWin.dll"
#
#         self.pm = Pymem("WeChat.exe")
#
#         self.bits = self.get_osbits()
#         self.version = self.get_file_version(self.process_name)
#         self.address_len = self.get_addr_len()
#
#         self.islogin = True
#
#     def get_addr_len(self):
#         version_nums = list(map(int, self.version.split(".")))  # 将版本号拆分为数字列表
#         if version_nums[0] <= 3 and version_nums[1] <= 9 and version_nums[2] <= 2:
#             return 4
#         else:
#             return 8
#
#     def find_all(self, c: bytes, string: bytes, base_addr=0):
#         """
#         查找字符串中所有子串的位置
#         :param c: 子串 b'123'
#         :param string: 字符串 b'123456789123'
#         :return:
#         """
#         return [base_addr + m.start() for m in re.finditer(re.escape(c), string)]
#
#     def get_file_version(self, process_name):
#         for process in psutil.process_iter(['pid', 'name', 'exe']):
#             if process.name() == process_name:
#                 file_version = Dispatch("Scripting.FileSystemObject").GetFileVersion(process.exe())
#                 return file_version
#         self.islogin = False
#
#     def get_osbits(self):
#         return int(platform.architecture()[0][:-3])
#
#     def search_memory_value(self, value: bytes, module_name="WeChatWin.dll"):
#         # 创建 Pymem 对象
#         pm = self.pm
#         module = pymem.process.module_from_name(pm.process_handle, module_name)
#
#         # result = pymem.pattern.pattern_scan_module(pm.process_handle, module, value, return_multiple=True)
#         # result = result[-1]-module.lpBaseOfDll if len(result) > 0 else 0
#         mem_data = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
#         result = self.find_all(value, mem_data)
#         result = result[-1] if len(result) > 0 else 0
#         return result
#
#     def search_key(self, key: bytes):
#         byteLen = self.address_len  # if self.bits == 32 else 8  # 4字节或8字节
#         key = re.escape(key)  # 转义特殊字符
#         key_addr = self.pm.pattern_scan_all(key, return_multiple=True)[-1] if len(key) > 0 else 0
#         key = key_addr.to_bytes(byteLen, byteorder='little', signed=True)
#         result = self.search_memory_value(key, self.module_name)
#         return result
#
#     def get_key_bias_test(self):
#         byteLen = self.address_len  # 4 if self.bits == 32 else 8  # 4字节或8字节
#         keyLenOffset = 0x8c if self.bits == 32 else 0xd0
#         keyWindllOffset = 0x90 if self.bits == 32 else 0xd8
#
#         pm = self.pm
#
#         module = pymem.process.module_from_name(pm.process_handle, "WeChatWin.dll")
#         keyBytes = b'-----BEGIN PUBLIC KEY-----\n...'
#         publicKeyList = pymem.pattern.pattern_scan_all(self.pm.process_handle, keyBytes, return_multiple=True)
#
#         keyaddrs = []
#         for addr in publicKeyList:
#             keyBytes = addr.to_bytes(byteLen, byteorder="little", signed=True)  # 低位在前
#             addrs = pymem.pattern.pattern_scan_module(pm.process_handle, module, keyBytes, return_multiple=True)
#             if addrs != 0:
#                 keyaddrs += addrs
#
#         keyWinAddr = 0
#         for addr in keyaddrs:
#             keyLen = pm.read_uchar(addr - keyLenOffset)
#             if keyLen != 32:
#                 continue
#             keyWinAddr = addr - keyWindllOffset
#             # keyaddr = int.from_bytes(pm.read_bytes(keyWinAddr, byteLen), byteorder='little')
#             # key = pm.read_bytes(keyaddr, 32)
#             # print("key", key.hex())
#
#         return keyWinAddr - module.lpBaseOfDll
#
#     def get_key_bias(self, wx_db_path, account_bias=0):
#         wx_db_path = os.path.join(wx_db_path, "Msg", "MicroMsg.db")
#         if not os.path.exists(wx_db_path):
#             return 0
#
#         def get_maybe_key(mem_data):
#             maybe_key = []
#             for i in range(0, len(mem_data), self.address_len):
#                 addr = mem_data[i:i + self.address_len]
#                 addr = int.from_bytes(addr, byteorder='little')
#                 # 去掉不可能的地址
#                 if min_addr < addr < max_addr:
#                     key = read_key(addr)
#                     if key == b"":
#                         continue
#                     maybe_key.append([key, i])
#             return maybe_key
#
#         def read_key(addr):
#             key = ctypes.create_string_buffer(35)
#             if ReadProcessMemory(pm.process_handle, void_p(addr - 1), key, 35, 0) == 0:
#                 return b""
#
#             if b"\x00\x00" in key.raw[1:33]:
#                 return b""
#
#             if b"\x00\x00" == key.raw[33:35] and b"\x90" == key.raw[0:1]:
#                 return key.raw[1:33]
#             return b""
#
#         def verify_key(keys, wx_db_path):
#             with open(wx_db_path, "rb") as file:
#                 blist = file.read(5000)
#             salt = blist[:16]
#             first = blist[16:DEFAULT_PAGESIZE]
#             mac_salt = bytes([(salt[i] ^ 58) for i in range(16)])
#
#             with multiprocessing.Pool(processes=8) as pool:
#                 results = [pool.apply_async(validate_key, args=(key, salt, first, mac_salt)) for key, i in keys[-1::-1]]
#                 results = [p.get() for p in results]
#                 for i, result in enumerate(results[-1::-1]):
#                     if result:
#                         return keys[i]
#                 return b"", 0
#
#         module_name = "WeChatWin.dll"
#         pm = self.pm
#         module = pymem.process.module_from_name(pm.process_handle, module_name)
#         start_addr = module.lpBaseOfDll
#         size = module.SizeOfImage
#
#         if account_bias > 1:
#             maybe_key = []
#             for i in [0x24, 0x40]:
#                 addr = start_addr + account_bias - i
#                 mem_data = pm.read_bytes(addr, self.address_len)
#                 key = read_key(int.from_bytes(mem_data, byteorder='little'))
#                 if key != b"":
#                     maybe_key.append([key, addr - start_addr])
#             key, bais = verify_key(maybe_key, wx_db_path)
#             if bais != 0:
#                 return bais
#
#         min_addr = 0xffffffffffffffffffffffff
#         max_addr = 0
#         for module1 in pm.list_modules():
#             if module1.lpBaseOfDll < min_addr:
#                 min_addr = module1.lpBaseOfDll
#             if module1.lpBaseOfDll > max_addr:
#                 max_addr = module1.lpBaseOfDll + module1.SizeOfImage
#
#         mem_data = pm.read_bytes(start_addr, size)
#         maybe_key = get_maybe_key(mem_data)
#         key, bais = verify_key(maybe_key, wx_db_path)
#         return bais
#
#     def run(self, is_logging=False, version_list_path=None):
#         self.version = self.get_file_version(self.process_name)
#         if not self.islogin:
#             error = "[-] WeChat No Run"
#             if is_logging: print(error)
#             return error
#         mobile_bias = self.search_memory_value(self.mobile)
#         name_bias = self.search_memory_value(self.name)
#         account_bias = self.search_memory_value(self.account)
#         # version_bias = self.search_memory_value(self.version.encode("utf-8"))
#
#         try:
#             key_bias = self.get_key_bias_test()
#         except:
#             key_bias = 0
#
#         if key_bias <= 0:
#             if self.key:
#                 key_bias = self.search_key(self.key)
#             elif self.db_path:
#                 key_bias = self.get_key_bias(self.db_path, account_bias)
#             else:
#                 key_bias = 0
#         rdata = {self.version: [name_bias, account_bias, mobile_bias, 0, key_bias]}
#         if version_list_path and os.path.exists(version_list_path):
#             with open(version_list_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 data.update(rdata)
#             with open(version_list_path, "w", encoding="utf-8") as f:
#                 json.dump(data, f, ensure_ascii=False, indent=4)
#         if is_logging:
#             print("{版本号:昵称,账号,手机号,邮箱,KEY}")
#             print(rdata)
#         return rdata


if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()
    parser.add_argument("--mobile", type=str, help="手机号", required=True)
    parser.add_argument("--name", type=str, help="微信昵称", required=True)
    parser.add_argument("--account", type=str, help="微信账号", required=True)
    parser.add_argument("--key", type=str, help="(可选)密钥")
    parser.add_argument("--db_path", type=str, help="(可选)已登录账号的微信文件夹路径")

    # 解析命令行参数
    args = parser.parse_args()

    # 检查是否缺少必要参数，并抛出错误
    if not args.mobile or not args.name or not args.account:
        raise ValueError("缺少必要的命令行参数！请提供手机号、微信昵称、微信账号。")

    # 从命令行参数获取值
    mobile = args.mobile
    name = args.name
    account = args.account
    key = args.key
    db_path = args.db_path

    # 调用 run 函数，并传入参数
    rdata = BiasAddr(account, mobile, name, key, db_path).run(True, "../version_list.json")
