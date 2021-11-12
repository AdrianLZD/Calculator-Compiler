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

def p_number(p):
    '''
    number : INUMBER
           | FNUMBER
           | ID 
    '''
    p[0] = p[1] #TODO set value of ID

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
        p[0] = p[2] if p[1] == '"' else str(p[1])[1:-1] + str(p[3])[1:-1]
    else:
        p[0] = p[1] #TODO Set value of id

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


def test_input(args):
    if args:
        print('Test: ' + str(args))
        if len(args) > 1:
            for arg in args[:-1]:
                yacc.parse(arg)
        return yacc.parse(args[len(args) - 1])
    else:
        print('[!] No arguments where received')









