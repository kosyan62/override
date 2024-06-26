int auth(char *username, int serial)
{
    int i;
    unsigned int hashed;
    int len;

    username[strcspn(username, "\n")] = 0;
    len = strnlen(username, 32);
    if (len <= 5 )
        return 1;
    if ( ptrace(PTRACE_TRACEME, 0, 1, 0) == -1 )
    {
        puts("\x1B[32m.---------------------------.");
        puts("\x1B[31m| !! TAMPERING DETECTED !!  |");
        puts("\x1B[32m'---------------------------'");
        return 1;
    }
    else
    {
        hashed = (username[3] ^ 0x1337) + 6221293;
        i = 0;
        while (i < len)
        {
            if (username[i] <= 31 )
                return 1;
            hashed += (hashed ^ username[i]) % 0x539;
            ++i;
        }
        return serial != hashed;
    }
}


int main(int argc, const char **argv, const char **envp)
{
    // Print banner
    puts("***********************************");
    puts("*\t\tlevel06\t\t  *");
    puts("***********************************");

    // Get username
    printf("-> Enter Login: ");
    char username[32];
    fgets(username, 32, stdin);
    puts("***********************************");
    puts("***** NEW ACCOUNT DETECTED ********");
    puts("***********************************");

    // Get serial
    printf("-> Enter Serial: ");

    unsigned int serial;
    scanf("%u", &serial);

    // Authenticate
    if (auth(username, serial) == 0)
    {
        puts("Authenticated!");
        system("/bin/sh");
        return 0;
    }
    return 1;
}