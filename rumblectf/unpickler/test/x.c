typedef unsigned long z;
typedef struct l { struct l *n; z v; } l;
typedef union { z z; char *s; l *l; _Bool b; int m; float f; } v;
void *malloc(z);
int printf(const char *, ...);
static void la(l **l, z v) {
    while (*l) l = &(*l)->n;
    *l = malloc(sizeof(struct l));
    (*l)->n = 0;
    (*l)->v = v;
}
static const int M = 0x1337;
int main(void) {
    v m[2] = {0};
    v s[3];
    z t = 0, a, b;
    v c;

    t++;
    s[t]=s[t-1];t++;
    m[1]=s[t-1];
    t++;
    s[t]=s[t-1];t++;
    printf("%#lx\n",s[--t].z);
}
