#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <number_to_check_against_rand>\n", argv[0]);
        return 1; 
    }

    int input_number = atoi(argv[1]);
    char *ht_pattern;
    if (argc == 2 ){
      ht_pattern = "";
    }
    else{
      ht_pattern = argv[2]; // The 'H' or 'T' pattern from the second argument
    }

    /*if (strlen(ht_pattern) != 6) {
        printf("The HT pattern must be exactly 5 characters long.\n");
        return 1;
    }*/

    int range_start = 0x65e70000;
    int range_end = 0x65f40000; 
    //int range_start = 12345;
    //int range_end = 12346; 

    printf("searching for %d\n", input_number);

    for (int i = range_start; i < range_end; ++i) {
        srand(i); 
        if ((rand() & 0x7fff) == input_number) {
            int found = 1;
            for (int j = 0; j < strlen(ht_pattern); ++j) {
                char expected = (rand() % 2 == 0) ? 'T' : 'H';
                if (ht_pattern[j] != expected) {
                    found = 0;
                    break; 
                }
            }
            if (found){
                printf("%d\n", i);
            }
        }
    }
    return 0;
}

