#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv) {
    if (argc <= 1) {
        printf("Usage: <flagtool> <writeflag/readflag>\nWrites flag to /root/\nUsed as SUID binary for CTF challenges\n");
        return -1;
    }

    setuid(0);
    setgid(0);
    seteuid(0);

	if(strcmp(argv[1], "writeflag") == 0) {
        char* FLAG_ENV = getenv("FLAG");
        if (FLAG_ENV == NULL) {
            printf("FLAG env not set\n");
            return -1;
        }

        FILE *f = fopen("/root/flag", "w");
        if (f == NULL)
        {
            printf("Error opening file!\n");
            exit(1);
        }

        /* print some text */
        fprintf(f, "%s\n", FLAG_ENV);
        fclose(f);
    }

    else if(strcmp(argv[1], "readflag") == 0) {
        char content[256];
        FILE *f = fopen("/root/flag", "r");
        if (f == NULL)
        {
            printf("Error opening file!\n");
            exit(1);
        }

        fgets(content, sizeof(content), f);

        /* print some text */
        printf("%s\n", content);
        fclose(f);
    }
    else {
        printf("Usage: <flagtool> <writeflag/readflag>\nWrites flag to /root/\nUsed as SUID binary for CTF challenges\n");
    }
}