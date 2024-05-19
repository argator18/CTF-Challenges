#include <stdio.h>
#include <stdint.h>

#define LICENSE_LENGTH 12 // Length of the license part we're iterating over

char license[LICENSE_LENGTH + 1] = {0}; // +1 for null terminator
long long count =0;
void process_license_combination() {
    // This function should implement the checking logic.
    // It's called for each combination of the license.
    // Example:
    // printf("%s\n", license);
      count ++;
      if (count %0x10000000 ==0){
        printf("\r0x%x",count);
        fflush(stdout);
      }
}

void iterate_combinations(int position) {
    if (position == LICENSE_LENGTH) {
        process_license_combination();
        return;
    }

    // Digits 0-9
    for (char c = '0'; c <= '9'; c++) {
        license[position] = c;
        iterate_combinations(position + 1);
    }

    // Letters A-Z
    for (char c = 'A'; c <= 'Z'; c++) {
        license[position] = c;
        iterate_combinations(position + 1);
    }
}

int main() {
    iterate_combinations(0); // Start iterating from the first position
    return 0;
}

