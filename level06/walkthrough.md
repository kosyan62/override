As usual first of all trying to run program, then open it in gdb.
It asks for user and serial, call function auth and if auth successful, call "/bin/sh".
This means that we can try not to right exploit but just find serial.
I attached disassembled code, so we can see that serial is read as unsigned int
and both username and serial used in function auth. In auth we see that username
shouldn't be less than 5, we have check for ptrace and in final simple hash function.
It's not a problem to avoid ptrace - just put breakpoint on syscall and change register after call,
so we can look at registers before cmp instruction. I used username "administrator",
set breakpoint on ptrace and put a breakpoint at address `0x8048866` (just before cmp) and for this username
right serial should be 6234238, we can find it in $ebp-0x10.
Use this without gdb and voilà.