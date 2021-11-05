import ply.lex as lex

literals = ['=', '+', '-', '*', '/', '^', '>', '<', '(', ')', '{', '}', ';']

keywords = {
    'boolean': 'BOOLEAN',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'and': 'AND',
    'or': 'OR',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'TRUE',
    'false': 'FALSE',
    'print': 'PRINT'
}

tokens = list(keywords.values()) + [
    'INUMBER',
    'FNUMBER',
    'ID',
    'EQUALS',
    'NOTEQUALS',
    'GTEQUALS',
    'LSEQUALS'
    'NEWLINE'
]

t_ignore = " \t"

t_INUMBER = r'\d+'
t_FNUMBER = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_GTEQUALS = r'>='
t_LSEQUALS = r'<='

def t_ID(t):
    r'[a-zA-Z_][\w]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()