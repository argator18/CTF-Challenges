#include <stdio.h>
#include <stdlib.h>

int main(){
  long *ptrs[10];

  for(int i =0; i < 10 ; i++){
    ptrs[i] = malloc(0x70);
  }
  for(int i = 0 ; i < 8 ; i ++){
    free(ptrs[i]);
  }
  //for(int i = 0;i<9;i++){
  //  printf("freed_pointer(%d) : %p\n",i,*ptrs[i]); 
  //}
  printf("test");
  printf("freed_pointer() : %p\n",*ptrs[7]); 
  printf("malloc : %p\n", &malloc);
}
