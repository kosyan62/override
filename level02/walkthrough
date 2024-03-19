We're dissassembling main in gdb and we can see that printf is executed with stack variable.
This means we probably can exploit it.
Let's try to run program with parameters, which will give us some stack.
We can use this little script to see what's in stack after printf call: `for(( i = 1; i < 42; i++)); do echo "$i - %$i\$p" | ./level02 | grep -a does; done`
if we change %$i\$p to %i\%c we will have some letters, but because of char we will have only one out of four.
If we will inspect output of script, we can see that probably there is 16 chars length null-teminated string. 
Our next step is to make it string. For that I wrote small script, let's run it. 
We have some letters let's try them
