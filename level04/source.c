int main()
{
    pid_t child = fork();
    char buf[128] = {0};
    int eip_val = 0;
    int status = 0;

    if(child == 0)
    {
        prctl(PR_SET_PDEATHSIG, SIGHUP);
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);

        puts("just give me some shellcode, k");
        gets(buf);
    }
    else
    {
        while(1)
        {
            wait(&status);
            if (WIFEXITED(status) || WIFSIGNALED(status)){
                puts("child is exiting...");
                break;
            }

            eip_val = ptrace(PTRACE_PEEKUSER, child, 0x2c, NULL);

            if(eip_val == 0xb)
            {
                printf("no exec() for you\n");
                kill(child, 9);
                break;
            }
        }
    }

    return EXIT_SUCCESS;
}