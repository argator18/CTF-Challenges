#!/usr/bin/env python

from pickletools import genops,dis
from tempfile import TemporaryDirectory
from os import system
import pickle


def main():
    pickle = bytes.fromhex(input("Pickle code (hex): "))
    


    stack_max = 0
    stack = []
    memo_cur = 0
    memo_max = 0
    code = []

    for opcode, arg, pos in genops(pickle):
        print(opcode.code,stack, opcode.stack_before)
        assert len(stack) >= len(opcode.stack_before)
        assert all(
            types_compatible(actual, expected)
            for actual, expected in zip(stack[-len(opcode.stack_before) :], opcode.stack_before)
        )
        stack = stack[: -len(opcode.stack_before)] + opcode.stack_after
        if len(stack) > stack_max:
            stack_max = len(stack)

        if opcode.code == "\x94":
            arg = memo_cur
        if opcode.code in "ghjpqr\x94" and int(arg) > memo_max:
            memo_max = int(arg)
        if opcode.code in "pqr\x94":
            memo_cur += 1

        if opcode.code in "IJKML\x8a\x8b":
            code.append(f"s[t++].z={int(arg)}")
        elif opcode.code in "STUBC\x8e\x96V\x8cX\x8d":
            code.append(f"s[t++].s=\"{repr(arg)[1:-1]}\"")
        elif opcode.code == "N":
            code.append("t++")
        elif opcode.code in "\x88\x89":
            arg = "01"[opcode.code == "\x89"]
            code.append(f"s[t++].b={arg}")
        elif opcode.code in "FG":
            code.append(f"s[t++].f={float(arg)}")
        elif opcode.code in "])":
            code.append("s[t++].l=0")
        elif opcode.code == "a":
            code.append("la(&s[t-1].l,s[t-2].z);t--")
        elif opcode.code == "e":
            code.append("a=t;while(s[--a].m!=M);b=a;while(++a<t)la(&s[b-1].l,s[a].z);t=b;")
        elif opcode.code in "lt":
            code.append("a=t;while(s[--a].m!=M);b=a;s[b].l=0;while(++a<t)la(&s[b].l,s[a].z);t=b+1;")
        elif opcode.code == "\x85":
            code.append("c=s[t-1];s[t-1].l=0;la(&s[t-1].l,c.z)")
        elif opcode.code == "\x86":
            code.append("c=s[t-2];s[t-2].l=0;la(&s[t-2].l,c.z);la(&s[t-2].l,s[t-1].z);t--")
        elif opcode.code == "\x87":
            code.append(
                "c=s[t-3];s[t-3].l=0;la(&s[t-3].l,c.z);la(&s[t-3].l,s[t-2].z);la(&s[t-3].l,s[t-1].z);t-=2"
            )
        elif opcode.code == "0":
            code.append("t--")
        elif opcode.code == "2":
            code.append("s[t]=s[t-1];t++")
        elif opcode.code == "(":
            code.append("s[t++].m=M")
        elif opcode.code == "1":
            code.append("while(s[--t].m!=M)")
        elif opcode.code in "ghj":
            code.append(f"s[t++]=m[{int(arg)}]")
        elif opcode.code in "pqr":
            code.append(f"m[{int(arg)}]=s[t-1]")
        elif opcode.code == "\x94":
            code.append(f"m[{memo_cur}]=s[t-1]")
        elif opcode.code == "\x80":
            pass
        elif opcode.code == ".":
            code.append('printf("%#lx\\n",s[--t].z)')
        else:
            print(b"unsupported opcode:" +  opcode.code.encode())
            exit()

    assert stack_max < 0x1000
    print(hex(memo_max))
    assert memo_max < 0x1000

    code = ";\n    ".join(code)

    code = f"""
typedef unsigned long z;
typedef struct l {{ struct l *n; z v; }} l;
typedef union {{ z z; char *s; l *l; _Bool b; int m; float f; }} v;
void *malloc(z);
int printf(const char *, ...);
static void la(l **l, z v) {{
    while (*l) l = &(*l)->n;
    *l = malloc(sizeof(struct l));
    (*l)->n = 0;
    (*l)->v = v;
}}
static const int M = 0x1337;
int main(void) {{
    v m[{memo_max+1}] = {{0}};
    v s[{stack_max+1}];
    z t = 0, a, b;
    v c;

    {code};
}}
    """
    code = code.strip() + "\n"

    with TemporaryDirectory() as t:
        t = "test"
        with open(f"{t}/x.c", "wt") as f:
            f.write(code)
        system(f"gcc -g -o '{t}/x' '{t}/x.c' && '{t}/x'")


def types_compatible(actual, expected):
    actual = actual.obtype
    if isinstance(actual, type):
        actual = (actual,)
    expected = expected.obtype

    return all(issubclass(a, expected) for a in actual)


if __name__ == "__main__":
    main()
