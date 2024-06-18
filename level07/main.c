#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int clear_stdin() {
    int result;

    do
        result = getchar();
    while (result != '\n' && result != -1);;
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

int store_number(unsigned int *tab) {
    unsigned int inp;
    unsigned int ind;

    printf(" Number: ");
    inp = get_unum();
    printf(" Index: ");
    ind = get_unum();
    if (ind % 3 == 0 || inp >> 24 == 183) {
        puts(" *** ERROR! ***");
        puts("   This ind is reserved for wil!");
        puts(" *** ERROR! ***");
        return 1;
    } else {
        tab[ind] = inp;
        return 0;
    }
}

int read_number(unsigned int *tab) {
    unsigned int inp;

    printf(" Index: ");
    inp = get_unum();
    printf(" Number at data[%u] is %u\n", inp, tab[inp]);
    return 0;
}

int main(int argc, const char **argv, const char **envp) {
    int result;
    char buff[20];
    unsigned int tab[100];
    int i;
    char *argv_p;
    char *envp_p;

    memset(buff, 0, 20);
    memset(tab, 0, 400);

    i = 0;
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

    puts(
            "----------------------------------------------------\n"
            "  Welcome to wil'tab crappy result storage service!   \n"
            "----------------------------------------------------\n"
            " Commands:                                          \n"
            "    store - store a result into the data storage    \n"
            "    read  - read a result from the data storage     \n"
            "    quit  - exit the program                        \n"
            "----------------------------------------------------\n"
            "   wil has reserved some storage :>                 \n"
            "----------------------------------------------------\n");
    while (1) {
        printf("Input command: ");
        result = 1;
        fgets(buff, 20, stdin);
        buff[strlen(buff) - 2] = 0;
        if (!memcmp(tab, "store", 5)) {
            result = store_number(tab);
        } else if (!memcmp(tab, "read", 4)) {
            result = read_number(tab);
        } else if (!memcmp(tab, "quit", 4))
            return 0;
        if (result)
            printf(" Failed to do %s command\n", buff);
        else
            printf(" Completed %s command successfully\n", buff);
        memset(buff, 0, 20);
    }
}