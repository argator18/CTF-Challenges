#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LICENSE_LENGTH 12 // Length of the license part we're iterating over

void increment_license(char *license) {
    int i = LICENSE_LENGTH - 2; // Start from the last character
    while (i >= 0) {
        if (license[i] == '9') { // If it's '9', switch to 'A'
            license[i] = 'A';
            break;
        } else if (license[i] == 'Z') { // If it's 'Z', reset to '0' and carry over
            license[i] = '0';
            i--; // Move to the next character to the left
            if (i == 9|| i == 5 || i ==1){
              i--;
            }
        } else { // Otherwise, just increment the character
            license[i]++;
            break;
        }
    }
}

uint32_t ROLD(uint32_t value, int8_t shift) {
    return (value << shift) | (value >> (32 - shift)); // Rotate left
}

  


uint32_t tar1, tar2, tar3, tar4;
uint32_t data_49f160[]= {
    0x07, 0x0c,	0x11, 0x16,
    0x07, 0x0c,	0x11, 0x16,
    0x07, 0x0c,	0x11, 0x16,
    0x07, 0x0c,	0x11, 0x16,
    0x05, 0x09, 0x0e, 0x14,
    0x05, 0x09,	0x0e, 0x14,
    0x05, 0x09,	0x0e, 0x14,
    0x05, 0x09,	0x0e, 0x14,
    0x04, 0x0b,	0x10, 0x17,
    0x04, 0x0b,	0x10, 0x17,
    0x04, 0x0b,	0x10, 0x17,
    0x04, 0x0b,	0x10, 0x17,
    0x06, 0x0a,	0x0f, 0x15,
    0x06, 0x0a,	0x0f, 0x15,
    0x06, 0x0a,	0x0f, 0x15,
    0x06, 0x0a,	0x0f, 0x15
};
uint32_t data_49f060[] = {
    0xd76aa478,	0xe8c7b756,	0x242070db,	0xc1bdceee,
    0xf57c0faf,	0x4787c62a,	0xa8304613,	0xfd469501,
    0x698098d8,	0x8b44f7af,	0xffff5bb1,	0x895cd7be,
    0x6b901122,	0xfd987193,	0xa679438e,	0x49b40821,
    0xf61e2562,	0xc040b340,	0x265e5a51,	0xe9b6c7aa,
    0xd62f105d,	0x2441453 , 0xd8a1e681,	0xe7d3fbc8,
    0x21e1cde6,	0xc33707d6,	0xf4d50d87,	0x455a14ed,
    0xa9e3e905,	0xfcefa3f8,	0x676f02d9,	0x8d2a4c8a,
    0xfffa3942,	0x8771f681,	0x6d9d6122,	0xfde5380c,
    0xa4beea44,	0x4bdecfa9,	0xf6bb4b60,	0xbebfbc70,
    0x289b7ec6,	0xeaa127fa,	0xd4ef3085,	0x4881d05,
    0xd9d4d039,	0xe6db99e5,	0x1fa27cf8,	0xc4ac5665,
    0xf4292244,	0x432aff97,	0xab9423a7,	0xfc93a039,
    0x655b59c3,	0x8f0ccc92,	0xffeff47d,	0x85845dd1,
    0x6fa87e4f,	0xfe2ce6e0,	0xa3014314,	0x4e0811a1,
    0xf7537e82,	0xbd3af235,	0x2ad7d2bb,	0xeb86d391
};

uint32_t license[] = {
            0x30303049, 0x30302d30, 0x80304e30, 0x0,
            0x0,        0x0,        0x0,        0x0,
            0x0,        0x0,        0x0,        0x0,
            0x0,        0x0,        0x58,       0x0
};

int check_license(){
    uint64_t rdx = 0; // Starting value of rdx, assumption
    uint64_t ret = 0; // Assuming ret is defined here
    
    tar1 = 0xefcdab89;
    tar2 = 0x98badcfe;
    tar3 = 0x10325476;
    tar4 = 0x67452301;

    while (1) {
        uint64_t val0 = rdx;
        uint32_t val_0 = rdx >> 4;
        int32_t res;

        if (val_0 == 1) {
            val0 = (((rdx * 5) + 1) & 0xf);
            res = ((tar1 ^ tar2) & tar3) ^ tar2;
        } else if (val_0 == 2) {
            val0 = (((val0 * 3) + 5) & 0xf);
            res = (tar1 ^ tar2) ^ tar3;
        } else if (val_0 == 0) {
            res = ((tar2 ^ tar3) & tar1) ^ tar3;
        } else {
            res = ((~tar3) | tar1) ^ tar2;
            val0 = (((val0 << 3) - val0) & 0xf);
        }

        int8_t fix1 = *(int8_t*)( (void*)data_49f160 + (rdx << 2));
        int32_t tmp_res = res + *(uint32_t*)(data_49f060 + rdx ) + *(uint32_t*)(license + val0) + tar4;

        rdx = rdx + 1;
        tar4 = tar3;
        ret = ROLD(tmp_res, fix1) + tar1;

        if (rdx == 0x40) break;

        tar3 = tar2;
        tar2 = tar1;
        tar1 = ret;
    }
    //printf("0x%x\n0x%x\n0x%x\n0x%x\n",ret,tar1,tar2,tar3);
    if (ret == 0x7b41bf6b &&tar1 == 0x3b3f6fc6 && tar2 ==0xbe8e4519 && tar3 == 0xd22413c4){
      return 1;
    }
    else{
      return 0;
    }
}



int main() {
    //char license[LICENSE_LENGTH + 1]= "X0XXX-XXXNX\x80"; // +1 for null terminator
    //for (int i = 0; i < LICENSE_LENGTH; i++) {
    //    license[i] = '0'; // Initialize license with '0'
    //}
    //license[LICENSE_LENGTH] = '\0'; // Null-terminate the string

    unsigned long long totalCombinations = 1;
    for (int i = 0; i < LICENSE_LENGTH; i++) {
        totalCombinations *= 36; // Each position can be 36 different values
    }

    for (unsigned long long count = 0; count < totalCombinations; count++) {
        // Here, you would insert the logic to check the license or perform computations with it.
        // For demonstration purposes, we're just printing each combination.
        //printf("%s\n", license);
        if (check_license()){
          printf("\nfound: %s\n",license);
        }
        if (count %0x100000 ==0){
          printf("\r0x%x : %s",count,license);
          fflush(stdout);
        }
        
        increment_license(license);
    }

    return 0;
}

