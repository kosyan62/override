void log_wrapper(FILE *file, char *msg, const char *filename) {
    char dest[264];

    strcpy(dest, msg);
    // On last position of dest, we add a filename from function args
    snprintf(&dest[strlen(dest)], 254 - strlen(dest), filename);
    // Change newline to null terminator
    dest[strcspn(dest, "\n")] = '\0';
    fprintf(file, "LOG: %s\n", dest);
}


int main(int argc, char **argv) {

    FILE *log_file;
    FILE *backup_file;
    int fd;
    int cur_char;
    char dest[104];

    cur_char = -1;
    if ( argc != 2 ) { // Check if we have 1 argument
        printf("Usage: %s filename\n", *argv);
    }
    log_file = fopen("./backups/.log", "w");
    if ( !log_file ) // Check if we can open log file
    {
        printf("ERROR: Failed to open %s\n", "./backups/.log");
        exit(1);
    }
    log_wrapper(log_file, "Starting back up: ", argv[1]);
    backup_file = fopen(argv[1], "r");
    if ( !backup_file ) // Check if we can open file to backup
    {
        printf("ERROR: Failed to open %s\n", argv[1]);
        exit(1);
    }
    strcpy(dest, "./backups/");
    strncat(dest, argv[1], 99 - strlen(dest));
    fd = open(dest, 193, 432);
    if ( fd < 0 ) // Check if we can open file to write backup
    {
        printf("ERROR: Failed to open %s%s\n", "./backups/", argv[1]);
        exit(1);
    }
    while ( 1 )
    {
        cur_char = fgetc(backup_file); // Read char from file
        if (cur_char == -1 )
            break;
        write(fd, &cur_char, 1); // Write char to dest file
    }
    log_wrapper(log_file, "Finished back up ", argv[1]);
    fclose(backup_file);
    close(fd);
    return 0;
}
