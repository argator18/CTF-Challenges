# lex_state2.py
#
# Declaration of a state for which no rules are defined

import sys
sys.path.insert(0,"..")

import ply.lex as lex

tokens = [ 
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

comment = 1
states = (('comment', 'exclusive'),)

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

# Comments
def t_comment(t):
    r'/\*'
    t.lexer.begin('comment')
    print "Entering comment state"

def t_comment_body_part(t):
    r'(.|\n)*\*/'
    print "comment body", t
    t.lexer.begin('INITIAL')

def t_error(t):
    pass

import sys

lex.lex()


