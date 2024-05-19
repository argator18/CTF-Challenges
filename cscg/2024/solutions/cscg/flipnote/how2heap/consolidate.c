#include <stdio.h>
#include <stdlib.h>

int main(){
  long *ptrs[9];

  for(int i =0; i < 7 ; i++){
    ptrs[i] = malloc(0x80);
  }
  for(int i = 0 ; i < 7 ; i ++){
    free(ptrs[i]);
  }
  long * tar = malloc(0x10000);
  free(tar);
}
