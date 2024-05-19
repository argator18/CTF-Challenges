#include <stdio.h>
#include <stdlib.h>

int main(){
  long *ptrs[9];

  for(int i =0; i < 9 ; i++){
    ptrs[i] = malloc(0x80);
  }
  for(int i = 0 ; i < 8 ; i ++){
    free(ptrs[i]);
  }
  long * tar = malloc(0x70);
  //for(int i = 0;i<9;i++){
  //  printf("freed_pointer(%d) : %p\n",i,*ptrs[i]); 
  //}
  printf("freed_pointer() : %p\n",*tar); 
  printf("malloc : %p\n", &malloc);
}
