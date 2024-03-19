#include <stdio.h>

int main()
{
    char *to_xor = "Q}|u`sfg~sf{}|a3";
    char new_str[17];
    printf("Checking all xors for numbers from 0 to 21\n");
    int i;
    int number = 0;

    new_str[16] = 0;
    while (number <= 21)
    {
        i = 0;
        while (to_xor[i] != 0)
        {
            new_str[i] = to_xor[i] ^ number;
            i++;
        }
        printf("String with num <%i>: %s\n", number, new_str);
        number++;
    }
}
