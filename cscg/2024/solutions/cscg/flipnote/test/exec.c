#include <stdio.h>
#include <unistd.h>

int main() {
    // Define the command to be executed
    char *args[] = {"/bin/sh", NULL};

    // Execute /bin/sh using execve
    if (execve("/bin/sh", args, NULL) == -1) {
        perror("execve");
        return 1; // Return error if execve fails
    }

    return 0;
}

