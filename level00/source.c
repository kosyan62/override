int32_t main(int32_t argc, char** argv, char** envp)
{
    puts("***********************************");
    puts("* \t     -Level00 -\t\t  *");
    puts("***********************************");
    printf("Password:");
    int32_t pincode;
    scanf("%d", &pincode);
    int32_t ret;
    if (pincode != 0x149c) // 5276
    {
        puts("\nInvalid Password!");
        ret = 1;
    }
    else
    {
        puts("\nAuthenticated!");
        system("/bin/sh");
        ret = 0;
    }
    return ret;
}
