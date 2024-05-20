# level00 walkthrough

Given 32-bit elf binary:

    $ file level00
    level00: setuid setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x20352633f776024748e9f8a5ebab6686df488bcf, not stripped

On execution the programm askas for a password:

    $ ./level00 
    ***********************************
    * 	     -Level00 -		  *
    ***********************************
    Password:1234

    Invalid Password!

Lets try to get the password from the binary using gdb disassembly:

    gdb ./level00
    (gdb) set dissassembly-flavor intel # view disassembly code in intel syntax
    (gdb) disass *main # disassemble main function
    Dump of assembler code for function main:
        0x08048494 <+0>:	push   ebp
        0x08048495 <+1>:	mov    ebp,esp
        0x08048497 <+3>:	and    esp,0xfffffff0
        0x0804849a <+6>:	sub    esp,0x20
        0x0804849d <+9>:	mov    DWORD PTR [esp],0x80485f0
        0x080484a4 <+16>:	call   0x8048390 <puts@plt>
        0x080484a9 <+21>:	mov    DWORD PTR [esp],0x8048614
        0x080484b0 <+28>:	call   0x8048390 <puts@plt>
        0x080484b5 <+33>:	mov    DWORD PTR [esp],0x80485f0
        0x080484bc <+40>:	call   0x8048390 <puts@plt>
        0x080484c1 <+45>:	mov    eax,0x804862c
        0x080484c6 <+50>:	mov    DWORD PTR [esp],eax
        0x080484c9 <+53>:	call   0x8048380 <printf@plt>
        0x080484ce <+58>:	mov    eax,0x8048636
        0x080484d3 <+63>:	lea    edx,[esp+0x1c]
        0x080484d7 <+67>:	mov    DWORD PTR [esp+0x4],edx
        0x080484db <+71>:	mov    DWORD PTR [esp],eax
        0x080484de <+74>:	call   0x80483d0 <__isoc99_scanf@plt>
        0x080484e3 <+79>:	mov    eax,DWORD PTR [esp+0x1c]
        0x080484e7 <+83>:	cmp    eax,0x149c
        0x080484ec <+88>:	jne    0x804850d <main+121>
        0x080484ee <+90>:	mov    DWORD PTR [esp],0x8048639
        0x080484f5 <+97>:	call   0x8048390 <puts@plt>
        0x080484fa <+102>:	mov    DWORD PTR [esp],0x8048649
        0x08048501 <+109>:	call   0x80483a0 <system@plt>
        0x08048506 <+114>:	mov    eax,0x0
        0x0804850b <+119>:	jmp    0x804851e <main+138>
        0x0804850d <+121>:	mov    DWORD PTR [esp],0x8048651
        0x08048514 <+128>:	call   0x8048390 <puts@plt>
        0x08048519 <+133>:	mov    eax,0x1
        0x0804851e <+138>:	leave  
        0x0804851f <+139>:	ret    
    End of assembler dump.

After a bunch of 'puts' we can spot a 'scanf' function call followed by a cmp instruction on the line main+83:

    0x080484e7 <+83>:	cmp    eax,0x149c

In this line register eax is being compared to the '0x149c' value which is a hex representation of the number '5276', let's try to put it as a password:

    $ ./level00 
    ***********************************
    * 	     -Level00 -		  *
    ***********************************
    Password:5276

    Authenticated!
    $ whoami
    level01

The binary executes shell under the 'level01' user, now we can just read the flag for the next level:

    $ cat /home/users/level01/.pass
    uSq2ehEGT6c9S24zbshexZQBXUGrncxn5sD5QfGL

Profit!
