import random
import math
from sympy import legendre_symbol, sqrt_mod, invert


p = 6679634264603989259674054716503969
a = 1
b = 1358889813528546611798772087239101
n = 6679634264603989344965977654561344

class Point:
    def __init__(self, X, Y, Z = 1, a = None, b = None, q = None):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.a = a
        self.b = b
        self.q = q
    
    

    def infinity(self = None):
        if self == None:
            return Point(0,1,0)
        return Point(0,1,0,self.a,self.b,self.q)

    def __repr__(self):
        if self.Z ==1:
            return f"Point({self.X}, {self.Y})"
        return f"Point({self.X}, {self.Y}, {self.Z})"

    def is_infinity(self):
        return self.X == 0 and self.Y != 0 and self.Z == 0

    def __add__(self, other):
        if self.a == None:
            print(f"Error: the point {self} doesn't contain any curve information")
            exit()
        return self.add(self, other, self.a)
    def __sub__(self,other):
        return self.__add__(other.negate())
    def negate(self):
        return Point(self.X, -self.Y, self.Z, self.a, self.b, self.q)

    def __rmul__(self,scalar):
        return self.__mul__(scalar)

    def __mul__(self, scalar):
        result = self.infinity()
        current = self
        while scalar > 0:
            if scalar % 2 == 1:
                result += current
            current += current
            scalar //= 2
        return result

    def make_affine(self):
        if self.is_infinity():
            print("Error")
            exit()
        self.X *= invert(self.Z,self.q)
        self.Y *= invert(self.Z,self.q)
        self.X %= self.q
        self.Y %= self.q
        self.Z = 1

    @staticmethod
    def add(P, Q, a):
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P
        if P.q != Q.q:
            print("Error!")
            exit()
        q = P.q
        
        P.make_affine()
        Q.make_affine()
        X1, Y1 = P.X, P.Y
        X2, Y2 = Q.X, Q.Y

        if X1 == X2 and Y1 == ((-Y2) % q):
            return P.infinity()

        if P == Q:
            slope = (3 * X1**2 + a ) * invert(2 * Y1,q)
            X3 = slope**2 - 2 * X1 
            Y3 = slope * (X1 - X3) - Y1
        else:
            slope = (Y2 - Y1) * invert(X2 - X1,q)
            X3 = slope**2 - X1 - X2
            Y3 = slope * (X1 - X3) - Y1
        X3 %= q
        Y3 %= q
        return Point(X3, Y3, a = P.a, b = P.b,q = P.q)
    

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.X * other.Z == other.X * self.Z and self.Y * other.Z == other.Y * self.Z
        return False

    # Task 1

    @staticmethod
    def sample_point(a, b, q):
        def coinflip():
            return random.choice([True,False])
        while True:
            x = random.randint(-q, q)
            if x == -q:
                x = 0
                y = -1
            elif x < 0:
                x = -x
                y = -1
            else:
                y = 1
            if x == q:
                return Point.infinity()
                
            y_squared = (pow(x, 3, q) + a*x + b) % q
            if legendre_symbol(y_squared, q) == 1:
                y = (y * sqrt_mod(y_squared, q)) % q

                if y == 0 and coinflip():
                   return sample_point() 
                return Point(x, y, a=a, b=b, q=q)
