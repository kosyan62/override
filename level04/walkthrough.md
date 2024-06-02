This task looks exactly like level01, but there is one extra.
The exploitable process will be child after fork, so we need to `set follow-fork-mode child` in gdb.
* Important note here: when starting gdb - better to unset all enviroments variables and use full path of binary.
After doing this, let's exploit gets. Basically, listing from screenshot telling that
32 dwords in stack variable is zeroed in beginning. It's 128 bytes array, so we will try something bigger.
We found that stack offset is 156. Also if we will try `info functions` in gdb, we can see `system`. It is
a way to use ret2libc method where we will change return address and stack variables for `system.exec(/bin/sh).
after this we can just add all addreses to script and craft `cat .pass` command to see our flag.
