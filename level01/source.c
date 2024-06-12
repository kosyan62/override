

int verify_user_name()
{
    puts("verifying username....\n");
    return (strncmp(a_user_name, "dat_wil", 7));
}


int verify_user_pass(char* pass)
{
    return (strncmp(pass, "admin", 5));
}

char a_user_name[80];

int32_t main(int32_t argc, char** argv, char** envp)
{
    char pass[68];
    
    memset(pass, 0, 64);
    puts("********* ADMIN LOGIN PROMPT ***…");
    printf("Enter Username: ");
    fgets(a_user_name, 256, stdin);
    int rc;
    if (verify_user_name() != 0)
    {
        puts("nope, incorrect username...\n");
        rc = 1;
    }
    else
    {
        puts("Enter Password: ");
        fgets(pass, 100, stdin);
        int valid = verify_user_pass(pass);
        if (valid == 0)
        {
            puts("nope, incorrect password...\n");
            rc = 1;
        }
        if (valid == 0)
        {
            rc = 0;
        }
    }
    return rc;
}
