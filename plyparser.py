import ply.yacc as yacc
import lexer
import operator

tokens = lexer.tokens


ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.xor,
}

def eqcomp(a, b):
    return a == b

def nqcomp(a, b):
    return a != b

def andcomp(a, b):
    a = str_to_bool(a)
    b = str_to_bool(b)
    return a and b

def orcomp(a, b):
    a = str_to_bool(a)
    b = str_to_bool(b)
    return a or b

def str_to_bool(a):
    if type(a) == bool: return a
    return a != ''
    
comps = {
    '==': eqcomp,
    '!=': nqcomp,
    'and': andcomp,
    'or': orcomp,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}


class Node:
    def __init__(self, type, children=[], parent=None, pType=None):
        self.type = type
        self.children = children
        self.parent = parent
        self.pType = pType

def p_script(p):
    '''
    script : block
    '''
    p[0] = p[1]


def p_block(p):
    '''
    block : stmt block
          | stmt
    '''
    if len(p) > 2 :
        p[0] = Node('block', p[2], [p[1]])
        print('missing')
        # TODO (Set parent hierarchy)
    else:
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : simstmt ';'
    '''
    p[0] = p[1]

def p_stmt_newline(p):
    '''
    stmt : NEWLINE
    '''
    p[0] = None

def p_simstmt_declaration(p):
    '''
    simstmt : INT ID
    simstmt : FLOAT ID
    simstmt : STRING ID
    simstmt : BOOLEAN ID
    '''
    p[0] = p[2]

def p_simstmt_assign(p):
    '''
    simstmt : INT ID '=' numexpr
    simstmt : FLOAT ID '=' numexpr
    simstmt : STRING ID '=' wordexpr
    simstmt : BOOLEAN ID '=' boolexpr
    '''
    p[0] = p[4]

def p_numexpr(p):
    '''
    numexpr : number
            | numexpr arit numexpr
    '''
    if len(p) > 2:
        p[0] = ops[p[2]](p[1], p[3])
    else:
        p[0] = p[1]

def p_number_id(p):
    '''
    number : ID 
    '''
    p[0] = p[1] #TODO set value of ID


def p_number_int(p):
    '''
    number : INUMBER 
    '''
    p[0] = int(p[1])


def p_number_float(p):
    '''
    number : FNUMBER 
    '''
    p[0] = float(p[1])

def p_arit(p):
    '''
    arit : '+'
         | '-'
         | '*'
         | '/'
         | '^'
    '''
    p[0] = p[1]

def p_wordexpr_word(p):
    '''
    wordexpr : WORD
    '''
    word = p[1][1:-1]
    length = len(word)
    i = 0
    while i < length:
        if word[i] == '\\':
            word = word[0: i:] + word[i+1: :]
            i += 1
        i += 1
    p[0] = word

def p_wordexpr_concats(p):
    '''
    wordexpr : ID
             | wordexpr '+' wordexpr
    '''
    if len(p) == 4:
        p[0] =  str(p[1]) + str(p[3])
    else:
        p[0] = p[1] #TODO Set value of id

def p_boolexpr_normal(p):
    '''
    boolexpr : TRUE
             | FALSE
    '''
    p[0] = eval(p[1].title())

def p_boolexpr_compar(p):
    '''
    boolexpr : compar
    '''
    p[0] = p[1]

def p_boolexpr_types(p):
    '''
    boolexpr : ID
    '''
    p[0] = True if float(p[1]) > 0 else False #TODO Fix ID declaration


def p_compar(p):
    '''
    compar : '(' comparexpr ')'
           | '(' boolexpr ')'
    '''
    p[0] = p[2]

def p_comparexpr(p):
    '''
    comparexpr : numexpr compbasic boolexpr
               | boolexpr compbasic numexpr
               | wordexpr compmin wordexpr
               | numexpr compall numexpr
               | comparexpr compall comparexpr
    '''
    for i in p:
        print(i)

    p[0] = comps[p[2]](p[1], p[3])

def p_comparexpr_bool_bool(p):
    '''
    comparexpr : boolexpr compbasic boolexpr
    '''
    p[0] = comps[p[2]](str_to_bool(p[1]), str_to_bool(p[3]))

def p_comparexpr_word_bool(p):
    '''
    comparexpr : wordexpr compmin boolexpr
    '''
    p[0] = comps[p[2]](p[1], str_to_bool(p[3]))

def p_comparexpr_bool_word(p):
    '''
    comparexpr : boolexpr compmin wordexpr
    '''
    p[0] = comps[p[2]](str_to_bool(p[1]), p[3])

def p_compall(p):
    '''
    compall : GTEQUALS
            | LSEQUALS
            | '>'
            | '<'
            | compbasic
    '''
    p[0] = p[1]

def p_compbasic(p):
    '''
    compbasic : AND
              | OR
              | compmin
    '''
    p[0] = p[1]


def p_compmin(p):
    '''
    compmin : EQUALS
            | NOTEQUALS
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" %(p.lexpos, p.lineno))
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        print(yacc.parse(s))


def test_tokens(args):
    if args:
        print('Test: ' + str(args))
        if len(args) > 1:
            for arg in args[:-1]:
                yacc.parse(arg)
        return yacc.parse(args[len(args) - 1])
    else:
        print('[!] No arguments where received')









