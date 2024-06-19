int clear_stdin() {
    char result = 0;

    while (1)
    {
        result = getchar();
        if (result == '\n' || result == -1)
            break;
    }
    return result;
}

unsigned int get_unum() {
    unsigned int input;

    input = 0;
    fflush(stdout);
    scanf("%u", &input);
    clear_stdin();
    return input;
}

int store_number(unsigned int *data) {
    unsigned int num = 0;
    unsigned int i = 0;

    printf(" Number: ");
    num = get_unum();

    printf(" Index: ");
    i = get_unum();

    if (i % 3 == 0 || num >> 24 == 183) {
        puts(" *** ERROR! ***");
        puts("   This ind is reserved for wil!");
        puts(" *** ERROR! ***");
        return 1;
    } else {
        data[i] = num;
        return 0;
    }
}

int read_number(unsigned int *data) {
    unsigned int i;

    printf(" Index: ");
    i = get_unum();
    printf(" Number at data[%u] is %u\n", i, data[i]);
    return 0;
}

int main(int argc, const char **argv, const char **envp) {
    int result;
    char input[20];
    unsigned int data[100];

    char *argv_p;
    char *envp_p;

    // Clearing input and data
    memset(input, 0, 20);
    memset(data, 0, 400);

    // Clearing argv and envp
    argv_p = (char *) argv;
    while (*argv_p) {
        memset(argv_p, 0, strlen(argv_p));
        ++argv_p;
    }
    envp_p = (char *) envp;
    while (*envp_p) {
        memset(envp_p, 0, strlen(envp_p));
        ++envp_p;
    }

    // Print welcome message
    puts(
            "----------------------------------------------------\n"
            "  Welcome to wil'data crappy result storage service!   \n"
            "----------------------------------------------------\n"
            " Commands:                                          \n"
            "    store - store a result into the data storage    \n"
            "    read  - read a result from the data storage     \n"
            "    quit  - exit the program                        \n"
            "----------------------------------------------------\n"
            "   wil has reserved some storage :>                 \n"
            "----------------------------------------------------\n");

    // Main loop
    while (1) {
        printf("Input command: ");
        result = 1;
        fgets(input, 20, stdin);
        input[strlen(input) - 2] = '\0';
        if (!memcmp(data, "store", 5))
            result = store_number(data);
        else if (!memcmp(data, "read", 4))
            result = read_number(data);
        else if (!memcmp(data, "quit", 4))
            return 0;
        if (result)
            printf(" Failed to do %s command\n", input);
        else
            printf(" Completed %s command successfully\n", input);
        memset(input, 0, 20);
    }
}