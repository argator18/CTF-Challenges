#!/usr/bin/env python3

import os
from secrets import randbelow, randbits

flag = os.getenv('FLAG', 'flag{redacted}')

class Chall:
    def __init__(self, nbits=2048):
        self.n = randbits(nbits)
        self.s = [randbelow(self.n) for _ in range(4)]
        self.B = self.n // (3*nbits)
        s = self.s
        #print((2 * s[0] + s[1] + s[2] + s[3]) % self.n)
        #print(s[0])
        #print("sum(s) + B",(s[0] + s[1] + s[2] + s[3] + self.B) % self.n)
        #print("hex(n)",hex(self.n>>2030))
        #print("hex(B)",hex(self.B>>2030))
        #print(self.s)
    
    def query(self, x):
        res = randbelow(self.B)
        assert len(x) == 4
        assert all((xi % self.n) != 0 for xi in x)
        s = self.s
        for si, xi in zip(self.s, x):
            res = (res + si*xi) % self.n
        return res


def main():
    print("I'm gonna send you a bunch of random numbers. But you can choose how random!")

    chall = Chall()
    print(f"The modulus is {chall.n}")

    for _ in range(10000):
        x = list(map(int, input("> ").strip().split(",")))
        #input()
        #x = [1,1,1,1]
        y = chall.query(x)
        #y -=  1 << (2048 - 12)
        #mask = (1 << 2048) - (1 << ( 2048 - 11))
        #print(hex(y & mask))
        print(y)
    
    guess = input("What's your guess? ")
    if guess == ",".join(map(str, chall.s)):
        print(flag)
        exit()
    assert chall.s[0] == guess.split(",")[0]
    assert chall.s[1] == guess.split(",")[1]
    assert chall.s[2] == guess.split(",")[2]
    assert chall.s[3] == guess.split(",")[3]
    #print(guess)
    #print()
    #print(",".join(map(str,chall.s)))
    print(guess.split(',')[0],chall.s[0])
    print(guess.split(',')[1],chall.s[1])
    print(guess.split(',')[2],chall.s[2])
    print(guess.split(',')[3],chall.s[3])


if __name__ == "__main__":
    main()
