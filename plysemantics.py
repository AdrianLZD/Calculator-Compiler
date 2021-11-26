import plyparser
import operator
import string
from util import logger
from util.node import Node
from util.symboltable import SymbolTable


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
    '<=' : operator.le,
    '==' : operator.eq,
    '!=' : operator.ne
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
    'while' : 'while',
    'print' : 'print'
}

toPrint = ''


def file_to_str(file):
    toStr = ''
    with open(file, 'r') as f:
        for line in f:
            toStr += line

    return toStr


def analize_semantics(input):
    try:
        parse_tree: Node = plyparser.parse_input(input)
    except SyntaxError as e:
        logger.error('[!] Parser failed.')
        raise e
    #print(parse_tree.print())
    symbol_table = SymbolTable('', None, {})
    try:
        symbol_table = create_block_table(parse_tree, symbol_table, 'm')
    except NameError as e:
        exit(0)

    return [parse_tree, symbol_table]


def create_block_table(node: Node, parent: SymbolTable, id):
    id_prefix = parent.id + '.' if parent.id != '' else parent.id
    table = SymbolTable(id_prefix + str(id), parent, {})
    for child in node.children:
        if child.type in var_declare:
            ref_type = search_variable(child.value, table, False)
            if ref_type != None:
                logger.error('[!] Semantic error.')
                logger.info('[?] Variable previously defined: ' + str(child.value) + '.')
                raise NameError("The variable " + child.value + " had already been defined.")
            
            if child.type == 'dint':
                validate_int(child, table, child.value)

            if child.children[0].type == 'id':
                assign_type = search_variable(child.children[0].value, table)
                if var_declare[child.type] == 'float' and assign_type == 'int':
                    table.children[child.value] = {'type': var_declare[child.type]}
                    continue

                if var_declare[child.type] != assign_type:
                    logger.error('[!] Semantic error.')
                    logger.info('[?] Can not assign a "' + assign_type + '" to a "' + var_declare[child.type] + '".')
                    raise NameError("Incompatible assignment.")

            elif child.children[0].type in comparators:
                validate_compar_types(child.children[0], table)

            table.children[child.value] = {'type': var_declare[child.type]}
            
        elif child.type in flowctrls:
            if child.type == 'if':
                block_if(child, table)
            elif child.type == 'for':
                block_for(child, table)
            elif child.type == 'while':
                block_while(child, table)
            elif child.type == 'print':
                validate_print(child, table)
                
        elif child.type == 'id':
            id_data = search_variable(child.value, table)
            if id_data == 'int':
                validate_int(child, table, child.value)
            table.children[child.value] = {'type' :id_data}

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


def validate_int(node: Node, scope: SymbolTable, assign: str):
    for child in node.children:
        raise_error = False
        if child.type == 'float':
            raise_error = True
        elif child.type == 'id':
            if search_variable(child.value, scope) == 'float':
                raise_error = True
        elif child.type in operators:
            validate_int(child, scope, assign)

        if raise_error:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "float" to integer "' + assign + '".')
            raise NameError('Incompatible declaration.')

    return True


def validate_compar_types(node: Node, scope: SymbolTable):
    child_types = [None, None]
    for i, child in enumerate(node.children):
        if child.type == 'id':
            child_types[i] = search_variable(child.value, scope)
        elif child.type in comparators:
            child_types[i] = validate_compar_types(child, scope)
        else:
            child_types[i] = child.type

    if child.parent.type in ['==', '!=']:
        is_number = False
        is_string = False
        if child_types[0] in ['int', 'float'] or child_types[1] in ['int', 'float']:
            is_number = True
        
        if child_types[0] == 'string' or child_types[1] == 'string':
            is_string = True

        if is_number and is_string:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not use "' + node.type + '" between numbers and strings.')
            raise NameError('Incompatible comparison.')
    elif not None in child_types:
        if child_types[0] == 'string' or child_types[1] == 'string':
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not use "' + node.type +'" to compare strings.')
            raise NameError('Incompatible comparison.')

    return True


def block_if(node: Node, parent: SymbolTable):
    for i, child in enumerate(node.children):
        if child.type == 'else':
            node_to_use = child.children[0]
        else:
            validate_compar_types(child, parent)
            node_to_use = child.children[1]

        parent.children['if' + str(parent.block_childs)] = create_block_table(node_to_use, parent, str(parent.block_childs) + 'if')
        parent.block_childs += 1
        


def block_for(node: Node, parent: SymbolTable):
    id_prefix = parent.id + '.' if parent.id != '' else parent.id
    table = SymbolTable(id_prefix + str(parent.block_childs) + 'for', parent, {})
    parent.children['for' + str(parent.block_childs)] = table
    
    # Declaration
    declare_child = node.children[0]
    assign_type = ''
    if declare_child.type == 'id':
        assign_type = search_variable(declare_child.value, table)

        if not assign_type in ['float', 'int']:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not use "' + assign_type + '" to traverse in a for loop.')
            raise NameError('Incompatible declaration.')

        if assign_type == 'int':
            validate_int(declare_child, table, declare_child.value)
    else:
        assign_type = search_variable(declare_child.value, table, False)

        if assign_type != None:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable previously defined: ' + str(declare_child.value) + '.')
            raise NameError("The variable " + declare_child.value + " had already been defined.")
        if declare_child.type == 'dint':
            validate_int(declare_child, table, declare_child.value)

        table.children[declare_child.value] = {'type': var_declare[declare_child.type]}
    
    

    # Condition
    validate_compar_types(node.children[1], table)
    
    # Instruction
    ins_type = search_variable(node.children[3].children[0].value, table)
    if not ins_type in ['int', 'float']:
        logger.error('[!] Semantic error.')
        logger.info('[?] Can not use a "' + ins_type + '" in a "for" declaration.')
        raise NameError('Incompatible expression.')
    
    #Create block
    child_block = create_block_table(node.children[2], table, str(parent.block_childs) + 'for')
    parent.children['for' + str(parent.block_childs)].children.update(child_block.children)
    parent.block_childs += 1


def block_while(node: Node, parent: SymbolTable):
    #Check comparison
    validate_compar_types(node.children[0], parent)
    #Create block
    parent.children['while' + str(parent.block_childs)] = create_block_table(node.children[0].children[1], parent, str(parent.block_childs) + 'while')
    parent.block_childs += 1


def validate_print(node: Node, scope: SymbolTable):
    child_types = [None, None]
    comparing = False
    for i, child in enumerate(node.children):
        if child.type == 'id':
            child_types[i] = search_variable(child.value, scope)
        elif child.type in comparators:
            child_types[i] = validate_compar_types(child, scope)
            comparing = True
        else:
            child_types[i] = child.type

    if comparing and (child_types[0] == 'string' or child_types[1] == 'string'):
        logger.error('[!] Semantic error.')
        logger.info('[?] Can not use "' + node.type + '" with string comparison.')
        raise NameError('Incompatible comparison.')


def test_input(input):
    analize_semantics(input)
    return 'good'


def test_input_file(file):
    input = file_to_str(file)
    test_input(input)


if __name__ == '__main__':
    input = file_to_str('input/basic.txt')
    try:
        print(analize_semantics(input)[1])
    except SyntaxError or NameError:
        pass
    
        
