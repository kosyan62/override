int decrypt(char key)
{
  unsigned int i; // [esp+20h] [ebp-28h]
  unsigned int size; // [esp+24h] [ebp-24h]
  char cipher[29]; // [esp+2Bh] [ebp-1Dh] BYREF

  strncpy(cipher, "Q}|u`sfg~sf{}|a3", 17);
  size = strlen(cipher);
  for (i = 0; i < size; ++i)
    cipher[i] ^= key;
  if (!strncmp(cipher, "Congratulations!", 17))
    return system("/bin/sh");
  else
    return puts("\nInvalid Password");
}

int test(int input, int base)
{
    int key = (base - input);
    int rc;
    switch (key)
    {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
        case 16:
        case 17:
        case 18:
        case 19:
        case 20:
        case 21:
        {
            rc = decrypt(key);
            break;
        }
        default:
            rc = decrypt(rand());
    }
    return rc;
}

int main(int argc, char** argv, char** envp)
{
    srand(time(NULL));
    puts("***********************************");
    puts("*\t\tlevel03\t\t**");
    puts("***********************************");
    printf("Password:");
    int input;
    scanf("%d", &input);
    test(input, 322424845);
    return 0;
}
