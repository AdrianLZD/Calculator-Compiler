import plyparser
import operator
import string
import logger
from node import Node
from symboltable import SymbolTable


operators = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '^' : operator.pow
}

comparators = {
    '>' : operator.gt,
    '<' : operator.lt,
    '>=' : operator.ge,
    '<=' : operator.le
}

var_types = {
    'int': 'int',
    'float': 'float',
    'string': 'string',
    'boolean': 'boolean'
}


var_declare = {
    'dint': 'int',
    'dfloat': 'float',
    'dstring': 'string',
    'dboolean': 'boolean'
}


var_cast = {
    'int' : int,
    'float' : float,
    'string' : str,
    'boolean' : bool
}

flowctrls = {
    'if' : 'if',
    'for' : 'for',
    'while' : 'while'
}

toPrint = ''


def file_to_str(file):
    toStr = ''
    with open(file, 'r') as f:
        for line in f:
            toStr += line

    return toStr


def create_symbols_table(input):
    try:
        parse_tree: Node = plyparser.parse_input(input)
    except SyntaxError as e:
        logger.error('[!] Parser failed.')
        raise e
    print(parse_tree.print())
    symbol_table = SymbolTable('', None, {})
    try:
        symbol_table = create_block_table(parse_tree, symbol_table, 'm')
    except NameError as e:
        exit(0)

    return symbol_table


def create_block_table(node: Node, parent: SymbolTable, id):
    child_blocks = 0
    id_prefix = parent.id + '.' if parent.id != '' else parent.id
    table = SymbolTable(id_prefix + str(id), parent, {})
    for child in node.children:
        if child.type in var_declare:
            ref_type = search_variable(child.value, table, False)
            if ref_type != None:
                logger.error('[!] Semantic error.')
                logger.info('[?] Variable previously defined: ' + str(child.value) + '.')
                raise NameError("The variable " + child.value + " had already been defined.")
            
            if child.children[0].type == 'id':
                assign_type = search_variable(child.children[0].value, table)
                if var_declare[child.type] != assign_type:
                    logger.error('[!] Semantic error.')
                    logger.info('[?] Can not assign a "' + assign_type + '" to a "' + var_declare[child.type] + '".')
                    raise NameError("Incompatible assignment.")

            elif child.children[0].type in comparators:
                check_compar_types(child.children[0], table)

            table.children[child.value] = {'type': var_declare[child.type]}
            
        elif child.type in flowctrls:
            child_blocks += 1
            if child.type == 'if':
                block_if(child, table, child_blocks)
            elif child.type == 'for':
                block_for(child, table, child_blocks)
            elif child.type == 'while':
                block_while(child, table, child_blocks)
                
        elif child.type == 'id':
            id_data = search_variable(child.value, table)
            table.children[child.value] = {'type' :id_data[0]}

    return table

# Retrieves the type of a variable
def search_variable(id : string, parent: SymbolTable, raiseException = True):
    if id in parent.children:
        return parent.children[id]['type']
    elif parent.parent != None:
        return search_variable(id, parent.parent, raiseException)
    else:
        if raiseException == True:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable not defined: ' + id + '.')
            raise NameError("Can not reference a variable not previously defined: " + id + '.')
        else:
            return None


def check_compar_types(node: Node, scope: SymbolTable):
    child_types = [None, None]
    for i, child in enumerate(node.children):
        if child.type == 'id':
            child_types[i] = search_variable(child.value, scope)
        elif child.type in comparators:
            child_types[i] = check_compar_types(child, scope)
        else:
            child_types[i] = child.type

    if child_types[0] == 'string' or child_types[1] == 'string':
        logger.error('[!] Semantic error.')
        logger.info('[?] Can not use "' + node.type +'" with strings.')
        raise NameError('Incompatible comparison.')

    return True

def block_if(node: Node, parent: SymbolTable, blocks: int):
    for i, child in enumerate(node.children):
        if child.type == 'else':
            node_to_use = child.children[0]
        else:
            check_compar_types(child, parent)
            node_to_use = child.children[1]
            
        block_id = str(i) + child.value
        parent.children['if' + str(blocks) + block_id] = create_block_table(node_to_use, parent, block_id)
        blocks += 1


def block_for(node: Node, parent: SymbolTable, blocks: int):
    id_prefix = parent.id + '.' if parent.id != '' else parent.id
    table = SymbolTable(id_prefix + str(blocks) + 'for', parent, {})
    parent.children['for' + str(blocks)] = table
    # Declaration
    declare_child = node.children[0]
    if declare_child.type == 'id':
        id_data = search_variable(declare_child.value, table)
        if not id_data in ['float', 'int']:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not use "' + id_data + '" to traverse in a for loop.')
            raise NameError('Incompatible declaration.')
    else:
        ref_type = search_variable(declare_child.value, table, False)
        if ref_type != None:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable previously defined: ' + str(declare_child.value) + '.')
            raise NameError("The variable " + declare_child.value + " had already been defined.")
        table.children[declare_child.value] = {'type': var_declare[declare_child.type]}
        #parent.children['for' + str(blocks)].children[declare_child.value] = {'type': var_declare[declare_child.type]}
    
    # Condition
    check_compar_types(node.children[1], table)
    
    # Instruction
    ins_type = search_variable(node.children[3].children[0].value, table)
    if not ins_type in ['int', 'float']:
        logger.error('[!] Semantic error.')
        logger.info('[?] Can not use a "' + ins_type + '" in a "for" declaration.')
        raise NameError('Incompatible expression.')
    #Create block
    child_block = create_block_table(node.children[2], table, blocks)
    parent.children['for' + str(blocks)].children.update(child_block.children)


def block_while(node: Node, parent: SymbolTable, blocks: int):
    #Check comparison
    if node.children[0].children[0].type in comparators:
        check_compar_types(node.children[0].children[0], parent)
        print(node.children[0].children[0].print())
    
    #Create block
    parent.children['while' + str(blocks)] = create_block_table(node.children[0].children[1], parent, str(blocks) + 'while')

def test_input(input):
    create_symbols_table(input)
    return 'good'

def test_input_file(file):
    input = file_to_str(file)
    test_input(input)


if __name__ == '__main__':
    input = file_to_str('input/basic.txt')
    try:
        print(create_symbols_table(input).print())
    except SyntaxError or NameError:
        pass
    
        
