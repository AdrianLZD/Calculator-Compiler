import ply.yacc as yacc
import plylexer
from util import logger
from util.node import Node
from ply.lex import LexError

tokens = plylexer.tokens

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
    if len(p) == 3 :
        p[0] = Node('block', 'block', [p[1]], None)
        p[1].parent = p[0]
        for child in p[2].children:
            p[0].children.append(child)
    else:
        p[0] = Node('block', 'empty')


def p_stmt(p):
    '''
    stmt : simstmt ';'
         | flowctrl
         | printstmt ';'
    '''
    p[0] = p[1]


def p_simstmt_assign(p):
    '''
    simstmt : INT ID '=' numstmt
            | INT ID '=' wordstmt
            | FLOAT ID '=' numstmt
            | FLOAT ID '=' wordstmt
            | STRING ID '=' numstmt
            | STRING ID '=' wordstmt
            | BOOLEAN ID '=' boolstmt
    '''
    p[0] = Node("d"+p[1], p[2], [p[4]])
    p[4].parent = p[0]


def p_simstmt_declaration(p):
    '''
    simstmt : INT ID
            | FLOAT ID
            | STRING ID
            | BOOLEAN ID
    '''
    if p[1] == 'int':
        child = Node('int', 0)
    elif p[1] == 'float':
        child = Node('float', 0.0)
    elif p[1] == 'string':
        child = Node('string', '')
    elif p[1] == 'boolean':
        child = Node('boolean', False)
    
    p[0] = Node("d"+p[1], p[2], [child])
    child.parent =p[0]


def p_simstmt_id(p):
    '''
    simstmt : ID '=' wordstmt 
            | ID '=' numstmt
            | ID '=' boolstmt
    '''
    p[0] = Node('id', p[1], [p[3]])
    p[3].parent = p[0]


def p_wordexpr_id(p):
    '''
    wordexpr : ID
    '''
    p[0] = Node('id', p[1])


def p_boolexpr_id(p):
    '''
    boolexpr : ID
    '''
    p[0] = Node('id', p[1])


def p_numstmt(p):
    '''
    numstmt : numexpr
    '''
    p[0] = p[1]


def p_numstmt_concat_wordstmt(p):
    '''
    numstmt : numstmt '+' wordstmt
            | wordstmt '+' numstmt
    '''
    p[0] = Node('+', '+', [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]


def p_numstmt_block(p):
    '''
    numstmt : '(' numexpr ')'
            | '(' numstmt ')'
    '''
    p[0] = p[2]


def p_numexpr(p):
    '''
    numexpr : number
    '''
    p[0] = p[1]


def p_wordexpr_concats(p):
    '''
    wordexpr : wordexpr '+' wordexpr
             | wordstmt '+' wordstmt
             | wordexpr '+' wordstmt
             | wordstmt '+' wordexpr
             | numexpr '+' wordexpr
             | wordexpr '+' numexpr
             | numexpr '+' wordstmt
             | wordstmt '+' numexpr
             | numstmt '+' wordexpr
             | wordexpr '+' numstmt
             | numstmt '+' wordstmt
             | wordstmt '+' numstmt
    '''
    p[0] = Node('+', '+', [p[1], p[3]])
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]

def p_numexpr_arit(p):
    '''
    numexpr : numexpr '+' numexpr
            | numstmt '+' numexpr
            | numexpr '+' numstmt
            | numstmt '+' numstmt
            | numexpr '-' numexpr
            | numstmt '-' numexpr
            | numexpr '-' numstmt
            | numstmt '-' numstmt
            | numexpr '*' numexpr
            | numstmt '*' numexpr
            | numexpr '*' numstmt
            | numstmt '*' numstmt
            | numexpr '/' numexpr
            | numstmt '/' numexpr
            | numexpr '/' numstmt
            | numstmt '/' numstmt
            | numexpr '^' numexpr
            | numstmt '^' numexpr
            | numexpr '^' numstmt
            | numstmt '^' numstmt
            
    '''
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]


def p_numexpr_uminus(p):
    '''
    numexpr : '-' numexpr %prec UMINUS
            | '+' numexpr %prec UMINUS
    '''
    if p[2].type == 'float' or p[2].type == 'int':
        p[2].value = p[1] + p[2].value
    else:
        child_found = False
        parent = p[2]
        while(not child_found):
            if parent.children[0].type == 'float' or parent.children[0].type == 'int':
                parent.children[0].value = p[1] + parent.children[0].value
                child_found = True
            else:
                parent = parent.children[0]
        
    p[0] = p[2]

def p_number_id(p):
    '''
    number : ID 
    '''
    p[0] = Node('id', p[1])


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


def p_wordstmt(p):
    '''
    wordstmt : wordexpr
    '''
    p[0] = p[1]


def p_wordstmt_num(p):
    '''
    wordstmt : '(' numexpr ')'
             | '(' wordexpr ')'
             | '(' wordstmt ')'
    '''
    p[0] = p[2]


def p_wordexpr_word(p):
    '''
    wordexpr : WORD
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


def p_boolstmt(p):
    '''
    boolstmt : boolexpr
    '''
    p[0] = p[1]


def p_boolstmt_block(p):
    '''
    boolstmt : '(' boolexpr ')'
             | '(' boolstmt ')'
    '''
    p[0] = p[2]


def p_boolexpr_normal(p):
    '''
    boolexpr : TRUE
             | FALSE
    '''
    p[0] = Node('boolean', eval(p[1].title()))


def p_boolexpr_types(p):
    '''
    boolexpr : boolcompar
    '''
    p[0] = p[1]


def p_boolexpr_compar(p):
    '''
    boolexpr : '(' compar ')'
    '''
    p[0] = p[2]


def p_boolcompar(p):
    '''
    boolcompar : boolstmt complogic boolstmt
               | boolstmt complogic numstmt
               | numstmt complogic boolstmt
               | numstmt complogic numstmt
    '''
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]


def p_complogic(p):
    '''
    complogic : AND
              | OR
    '''
    p[0] = p[1]


def p_compar(p):
    '''
    compar : comparexpr
           | boolexpr
    '''
    p[0] = p[1]


def p_comparexpr(p):
    '''
    comparexpr : numstmt compall boolstmt
               | boolstmt compall numstmt
               | wordstmt compmin wordstmt
               | numstmt compall numstmt
               | comparexpr compall comparexpr
               | boolstmt compall boolstmt
               | wordstmt compall boolstmt
               | boolstmt compall wordstmt
               | wordstmt compall numstmt
               | numstmt compall wordstmt
    '''
    p[0] = Node(p[2], p[2], [p[1], p[3]])
    p[1].parent = p[0]
    p[3].parent = p[0]


def p_compall(p):
    '''
    compall : GTEQUALS
            | LSEQUALS
            | '>'
            | '<'
            | compmin
    '''
    p[0] = p[1]


def p_compmin(p):
    '''
    compmin : EQUALS
            | NOTEQUALS
    '''
    p[0] = p[1]


def p_flowctrl_if(p):
    '''
    flowctrl : ifstmt
             | whilestmt
             | forstmt
    '''
    p[0] = p[1]


def p_ifstmt(p):
    '''
    ifstmt : IF ifblock
    '''
    p[0] = p[2]


def p_ifstmt_else(p):
    '''
    ifstmt : IF ifblock elseblock
    '''
    p[2].children.append(p[3])
    p[3].parent = p[2]
    p[0] = p[2]


def p_if_block_condition(p):
    '''
    ifblock : compblock
    '''
    p[0] = Node('if', 'if', [p[1]])
    p[1].parent = p[0]


def p_if_elif_block(p):
    '''
    ifblock : ifblock elifblock
    '''
    p[1].children.append(p[2])
    p[2].parent = p[1]
    p[0] = p[1]


def p_elif_block(p):
    '''
    elifblock : ELIF compblock
    '''
    p[0] = p[2]


def p_else_block(p):
    '''
    elseblock : ELSE '{' block '}'
    '''
    p[0] = Node(p[1], p[1], [p[3]])
    p[3].parent = p[0]


def p_whilestmt_condition(p):
    '''
    whilestmt : WHILE compblock
    '''
    p[0] = Node(p[1], p[1], [p[2]])
    p[2].parent = p[0]


def p_for_stmt(p):
    '''
    forstmt : FOR '(' fordeclare ';' compar ';' forins ')' '{' block '}'
    '''
    condition = Node('cond', 'cond', [p[5]])
    p[5].parent = condition
    p[0] = Node(p[1], p[1], [p[3], condition, p[10], p[7]])
    p[3].parent = p[0]
    condition.parent = p[0]
    p[10].parent = p[0]
    p[7].parent = p[0]


def p_for_declare_simple(p):
    '''
    fordeclare : INT ID
               | FLOAT ID
    '''
    if p[1] == 'int':
        child = Node('int', 0)
    elif p[1] == 'float':
        child = Node('float', 0.0)
    p[0] = Node('d' + p[1], p[2], [child])
    child.parent = p[0]


def p_for_declare_value(p):
    '''
    fordeclare : INT ID '=' numstmt
               | FLOAT ID '=' numstmt
    '''
    p[0] = Node('d' + p[1], p[2], [p[4]])
    p[4].parent = p[0]


def p_for_declare_id(p):
    '''
    fordeclare : ID '=' numstmt
    '''
    p[0] = Node('id', p[1], [p[3]])
    p[3].parent = p[0]
    

def p_for_instruction(p):
    '''
    forins : ID '+' '+'
           | ID '-' '-'
    '''
    oneNode = Node('int', 1)          
    idNode = Node('id', p[1])
    p[0] = Node(p[2], p[2], [idNode, oneNode])
    idNode.parent = p[0]
    oneNode.parent = p[0]


def p_comp_block(p):
    '''
    compblock : condblock
              | comparblock
    '''
    p[0] = p[1]


def p_cond_block(p):
    '''
    condblock : '(' boolstmt ')' '{' block '}'
              | '(' numstmt ')' '{' block '}'
              | '(' wordstmt ')' '{' block '}'
    '''
    p[0] = Node('cond', 'cond', [p[2], p[5]])
    p[2].parent = p[0]
    p[5].parent = p[0]


def p_compar_block(p):
    '''
    comparblock : '(' compar ')' '{' block '}'
    '''
    p[0] = Node('cond', 'cond', [p[2], p[5]])
    p[2].parent = p[0]
    p[5].parent = p[0]


def p_printstmt(p):
    '''
    printstmt : PRINT '(' printexpr ')'
    '''
    p[0] = Node(p[1], p[1], [p[3]])
    p[3].parent = p[0]


def p_printexpr(p):
    '''
    printexpr : wordstmt
              | numstmt
              | boolstmt
              | compar
    '''
    p[0] = p[1]


def p_printexpr_id(p):
    '''
    printexpr : ID
    '''
    p[0] = Node('id', p[1])


def p_error(p):
    if p:
        logger.error("[!] Syntax Error.")
        logger.info("[?] Illegal character: " + str(p))
        raise SyntaxError('Illegal character.')
    else:
        logger.error("[!] Syntax error at EOF: A bracket or semicolon is missing.")
        raise SyntaxError('A bracket or semicolon is missing.')


def test_tokens(arg):
    if arg:
        print('Test: ' + str(arg))
        res = yacc.parse(arg)
        return res if res == None else res.print_basic_test()
    else:
        print('[!] No arguments where received')


def test_tokens_parents(arg):
    if arg:
        print('Test: ' + str(arg))
        res = yacc.parse(arg)
        return res if res == None else res.print_parent_test()
    else:
        print('[!] No arguments where received')


def parse_input(input):
    return yacc.parse(input)


parser = yacc.yacc()
if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        try:
            res = yacc.parse(s)
            out = res if res == None else res.print_parent_test() + '\n' + res.print()
            #out = res if res == None else res.print_basic_test() + '\n' + res.print()
            #out = res if res == None else res.print()
            print(out)
        except LexError:
            print(s + ' is not a valid input')








