# -----------------------------------------------------------------------------
# yacc_sr.py
#
# A grammar with shift-reduce conflicts
# -----------------------------------------------------------------------------
import sys
sys.tracebacklimit = 0

sys.path.insert(0,"..")
import ply.yacc as yacc

from calclex import tokens

# Parsing rules

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print t[1]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[3] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print "Undefined name '%s'" % t[1]
        t[0] = 0

def p_error(t):
    print "Syntax error at '%s'" % t.value

yacc.yacc()




