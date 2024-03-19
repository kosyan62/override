I started from disassembling main in gdb.
We can figure out, that program reading decimal from stdin using scanf and then running function 'test' with input.
If we will continue to dig in we will figure out, that in function test we have only 21 possible values.
They will be created out of number `322424845` minus our input. Basically, we will send one of numbers to the function decrypt.
Now I struggled a bit, but I made some cleaning in decompilled function decrypt and atteched it. To check password it use xor for each symbol of static string and then compares it with "Congadulation". So we need to check this sting with all possible numbers. I wrote script for it and attached it and result too. 
We can see that we need 322424845 - 18 to pass the check. We can try it and after `whoami` see that we're succeed.
