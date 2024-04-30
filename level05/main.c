#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main()
{  
   int fd;
   char buff[1024];
   char path[] = "/home/users/level06/.pass";

   fd = open(path, O_RDONLY);
   read(fd, buff, 1024);

   printf("\n\n%s\n\n",buff);
}

