After exploiting binary, we can see that we have gets and wrong printf after it.
We can check it by passing `python -c 'print "ABCD" + "%x-" * 10' | ./level05`.
We will find start of our input on 10th position in printf output.
Let's start gdb now `env -i PWD=$PWD SHELL=$SHELL SHLVL=$SHLVL LINES=211 COLUMNS=53 /usr/bin/gdb $PWD/level05`
Here we can examine GOT table and find address of exit(). After it we will be able to craft proper exploit.
By putting exit addres we can change it's value in GOT table. Printf will put the amount of bytes written, so we just need to fill
our string with right payload. For this reason I wrote a script which crates special input string.