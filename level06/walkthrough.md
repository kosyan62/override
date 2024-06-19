# Level06 walkthrough

As usual first of all trying to run program, then open it in gdb.

It asks for username and serial, call function auth and if auth successful, call "/bin/sh".
This means that we can try not to wright exploit but just find serial.

In attached disassembled code, we can see that serial is read as unsigned int
and both username and serial used in function auth.
In auth we see that username shouldn't be less than 5, we have check for ptrace and in final simple hash function.

It's not a problem to avoid ptrace - just put breakpoint on syscall and change register after call,
so we can look at registers before cmp instruction.
```gdb
set disassembly-flavor intel
b *0x08048866
catch syscall ptrace
Catchpoint 1 (returned from syscall ptrace), 0xf7fdb435 in __kernel_vsyscall ()
(gdb) set $eax=0
(gdb) c
Continuing.
```
Here are breakpoint on ptrace and breakpoint at address `0x8048866` (just before cmp). With username
"administrator" right serial should be 6234238, we can find it in `$ebp-0x10`.
Use this login-serial pair without gdb and voilà.
