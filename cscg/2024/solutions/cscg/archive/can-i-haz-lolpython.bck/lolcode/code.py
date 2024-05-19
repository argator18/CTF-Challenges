# LOLPython to Python converter version 1.0
# Written by Andrew Dalke, who should have been working on better things.


# sys is used for COMPLAIN and ARGZ
import sys as _lol_sys

if __name__ == '__main__' :
    test = '/flag.txt' 
    print >>_lol_sys.stderr, open ( test ) . read ()

# The end.
