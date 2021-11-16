import ply.yacc as yacc
import lexer
import operator
from plynode import Node

tokens = lexer.tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('right', 'UMINUS')
)


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


def p_script(p):
    '''
    script : block
    '''
    p[0] = p[1]


def p_block(p):
    '''
    block : stmt block
          |
    '''
    if len(p) > 1 :
        p[0] = Node('block', 'block', [p[1]])
        p[1].parent = p[0]
        for child in p[2].children:
            p[0].children.append(child)
    else:
        p[0] = Node('ERROR', 'ERROR')

def p_stmt(p):
    '''
    stmt : simstmt ';'
    '''
    p[0] = p[1]

def p_stmt_newline(p):
    '''
    stmt : NEWLINE
         | 
    '''
    p[0] = None

def p_simstmt_declaration(p):
    '''
    simstmt : INT ID
    simstmt : FLOAT ID
    simstmt : STRING ID
    simstmt : BOOLEAN ID
    '''
    if p[1] == 'int':
        child = Node('int', 0)
    elif p[1] == 'float':
        child = Node('float', 0.0)
    elif p[1] == 'string':
        child = Node('string', '')
    elif p[1] == 'boolean':
        child = Node('boolean', False)
    
    p[0] = Node(p[1], p[2], [child])
    child.parent =p[0]



def p_simstmt_assign(p):
    '''
    simstmt : INT ID '=' numstmt
    simstmt : FLOAT ID '=' numstmt
    simstmt : STRING ID '=' wordstmt
    simstmt : BOOLEAN ID '=' boolexpr
    '''
    p[0] = Node(p[1], p[2], [p[4]])
    p[4].parent = p[0]

def p_numstmt(p):
    '''
    numstmt : numexpr
    '''
    p[0] = p[1]

def p_numstmt_block(p):
    '''
    numstmt : '(' numexpr ')'
    '''
    p[0] = p[2]

def p_numexpr(p):
    '''
    numexpr : number
    '''
    p[0] = p[1]

def p_numexpr_arit(p):
    '''
    numexpr : numexpr arit numexpr
            | numstmt arit numexpr
            | numexpr arit numstmt
            | numstmt arit numstmt
    '''
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]

def p_numexpr_uminus(p):
    '''
    numexpr : '-' numexpr %prec UMINUS
            | '+' numexpr %prec UMINUS
    '''
    ""
    if p[2].type == 'float' or p[2].type == 'int':
        p[2].value = p[1] + p[2].value
    else:
        p[2].children[0].value = p[1] + p[2].children[0].value
        
    p[0] = p[2]

def p_number_id(p):
    '''
    number : ID 
    '''
    p[0] = p[1] #TODO set value of ID


def p_number_int(p):
    '''
    number : INUMBER 
    '''
    p[0] = Node('int', p[1])


def p_number_float(p):
    '''
    number : FNUMBER 
    '''
    p[0] = Node('float', p[1])

def p_arit(p):
    '''
    arit : '+'
         | '-'
         | '*'
         | '/'
         | '^'
    '''
    p[0] = p[1]


def p_wordstmt(p):
    '''
    wordstmt : wordexpr
    '''
    p[0] = p[1]

def p_wordstmt_num(p):
    '''
    wordstmt : '(' numexpr ')'
    '''
    p[0] = p[2]


def p_wordexpr_word(p):
    '''
    wordexpr : WORD
             | ID
    '''
    word = p[1][1:-1]
    length = len(word)
    wordFix = ''
    i = 0
    while i < length:
        if word[i] == '\\':
            wordFix += word[i+1]
            i += 1
        else:
            wordFix += word[i]
        i += 1
    p[0] = Node('string', wordFix)

def p_wordexpr_concats(p):
    '''
    wordexpr : wordexpr '+' wordexpr
             | wordstmt '+' wordstmt
             | wordexpr '+' wordstmt
             | wordstmt '+' wordexpr
    '''
    if len(p) == 4:
        p[0] =  Node('+', '+', [p[1], p[3]])
        p[0] = Node(p[2], p[2], [p[1], p[3]])
        p[1].parent = p[0]
        p[3].parent = p[0]
    else:
        print("FIX")
        p[0] = p[1] #TODO Set value of id


def p_boolexpr_normal(p):
    '''
    boolexpr : TRUE
             | FALSE
    '''
    p[0] = Node('boolean', eval(p[1].title()))


def p_boolexpr_types(p):
    '''
    boolexpr : ID
    '''
    p[0] = True if float(p[1]) > 0 else False  # TODO Fix ID declaration

def p_boolexpr_compar(p):
    '''
    boolexpr : '(' compar ')'
    '''
    p[0] = p[2]

def p_compar(p):
    '''
    compar : comparexpr
           | boolexpr
    '''
    p[0] = p[1]

def p_comparexpr(p):
    '''
    comparexpr : numstmt compall boolexpr
               | boolexpr compall numstmt
               | wordexpr compall wordexpr
               | numstmt compall numstmt
               | comparexpr compall comparexpr
               | boolexpr compall boolexpr
               | wordexpr compall boolexpr
               | boolexpr compall wordexpr
    '''
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[3]

# def p_comparexpr_bool_bool(p):
#     '''
#     comparexpr : 
#     '''
#     p[0] = comps[p[2]](str_to_bool(p[1]), str_to_bool(p[3]))

# def p_comparexpr_word_bool(p):
#     '''
#     comparexpr :
#     '''
#     p[0] = comps[p[2]](p[1], str_to_bool(p[3]))

# def p_comparexpr_bool_word(p):
#     '''
#     comparexpr : 
#     '''
#     p[0] = comps[p[2]](str_to_bool(p[1]), p[3])

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
        print("Syntax error at line '%s' character '%s'" %(p.lineno, p.lexpos))
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
        res = yacc.parse(s)
        out = res if res == None else res.print_test() +'\n'+ res.print()
        #out = res if res == None else res.print()
        print(out)


def test_tokens(arg):
    if arg:
        print('Test: ' + str(arg))
        res = yacc.parse(arg)
        return res if res == None else res.print_test()
    else:
        print('[!] No arguments where received')









