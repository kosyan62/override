#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char buff[100];
    unsigned int i;

    i = 0;
    fgets(buff, 100, stdin);
    for ( i = 0; i < strlen(buff); ++i )
    {
        if (buff[i] > 'A' && buff[i] <= 'Z' )
            buff[i] ^= 0x20;
    }
    printf(buff);
    exit(0);
}