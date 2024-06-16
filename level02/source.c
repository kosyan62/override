int32_t main(int32_t argc, char** argv, char** envp)
{
    char user[96];
    memset(user, 0, 96);
    char auth[40];
    memset(auth, 0, 40);
    char pass[96];
    memset(pass, 0, 96);
    FILE* fp = fopen("/home/users/level03/.pass", "r");
    if (fp == 0)
    {
        fwrite("ERROR: failed to open password file", 1, 36, stderr);
        exit(1);
    }
    int auth_size = fread(auth, 1, 41, fp);
    *(auth + strcspn(auth, "\n")) = 0;
    if (auth_size != 41)
    {
        fwrite("ERROR: failed to read password file", 1, 36, stderr);
        fwrite("ERROR: failed to read password file", 1, 36, stderr);
        exit(1);
    }
    fclose(fp);
    puts("===== [ Secure Access System v1.0 ] =====");
    puts("/***************************************\\");
    puts("| You must login to access this system. |");
    puts("\\**************************************/");
    printf("--[ Username: ");
    fgets(user, 96, stdin);
    *(user + strcspn(user, "\n")) = 0;
    printf("--[ Password: ");
    fgets(pass, 96, stdin);
    *(pass + strcspn(pass, "\n")) = 0;
    puts("*****************************************");
    if (strncmp(auth, pass, 41) != 0)
    {
        printf(user);
        puts(" does not have access!");
        exit(1);
    }
    printf("Greetings, %s!\n", user);
    system("/bin/sh");
    return 0;
}
