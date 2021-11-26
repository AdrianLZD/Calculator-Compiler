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

logic_compar = {
    'or' : 'or',
    'and' : 'and'
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
            ref_type = search_variable_type(child.value, table, False)
            if ref_type != None:
                logger.error('[!] Semantic error.')
                logger.info('[?] Variable previously defined: ' + str(child.value) + '.')
                raise NameError("The variable " + child.value + " had already been defined.")
            
            if child.type == 'dint':
                validate_int(child, table, child.value)
            elif child.type == 'dfloat':
                validate_float(child, table, child.value)
            elif child.type == 'dstring':
                validate_string(child, table, child.value)
            elif child.type == 'dboolean':
                validate_boolean(child, table, child.value)

            if child.children[0].type == 'id':
                assign_type = search_variable_type(child.children[0].value, table)
                if var_declare[child.type] == 'float' and assign_type == 'int':
                    table.children[child.value] = {'type': var_declare[child.type]}
                    continue

                if var_declare[child.type] != assign_type:
                    logger.error('[!] Semantic error.')
                    logger.info('[?] Can not assign a "' + assign_type + '" to a "' + var_declare[child.type] + '".')
                    raise NameError("Incompatible assignment.")

            elif child.children[0].type in comparators or child.children[0].type in logic_compar:
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
            id_data = search_variable_type(child.value, table)
            if id_data == 'int':
                validate_int(child, table, child.value)
            elif id_data == 'float':
                validate_float(child, table, child.value)
            elif id_data == 'string':
                validate_string(child, table, child.value)
            elif id_data == 'boolean':
                validate_boolean(child, table, child.value)
            table.children[child.value] = {'type' :id_data}

    return table

# Retrieves the type of a variable
def search_variable_type(id : string, parent: SymbolTable, raiseException = True):
    if id in parent.children:
        return parent.children[id]['type']
    elif parent.parent != None:
        return search_variable_type(id, parent.parent, raiseException)
    else:
        if raiseException == True:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable not defined: ' + id + '.')
            raise NameError("Can not reference a variable not previously defined: " + id + '.')
        else:
            return None


def validate_int(node: Node, scope: SymbolTable, assign: str):
    type_error = 'float'
    raise_error = False
    for child in node.children:
        if child.type == 'float' or child.type == 'string':
            raise_error = True
            type_error = child.type
        elif child.type == 'id':
            type_error = search_variable_type(child.value, scope)
            if type_error != 'int':
                raise_error = True
            else:
                type_error = 'float'
        elif child.type in operators:
            validate_int(child, scope, assign)
       
        if raise_error:
            print(child)
            print(node)
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "' + type_error +'" to integer "' + assign + '".')
            raise NameError('Incompatible declaration.')

    return True


def validate_float(node: Node, scope: SymbolTable, assign: str):
    raise_error = False
    for child in node.children:
        if child.type == 'id':
            type_error = search_variable_type(child.value, scope)
            if not type_error in ['int', 'float']:
                raise_error = True

        if raise_error:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "' + type_error +'" to float "' + assign + '".')
            raise NameError('Incompatible declaration.')

    return True


def validate_arithmetic(node: Node, scope: SymbolTable, assign: str):
    operate = [node.children[0].value, node.children[1].value]
    child_types = [node.children[0].type, node.children[1].type]

    # Find id types if needed
    for i in range(2):
        if child_types[i] == 'id':
            child_types[i] = search_variable_type(operate[i], scope)

    # # Helps to detect when integers should be casted to floats
    # for i in range(2):
    #     if not float_operation:
    #         if child_types[i] == 'float':
    #             float_operation = True
    #         elif child_types[i] in operators:
    #             float_operation = is_float_operation(node.children[i], scope)

    for i in range(2):
        if child_types[i] in ['boolean', 'string']:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not operate a "' + child_types[i] +'" with a number.')
            raise NameError('Incompatible declaration.')
        if child_types[i] in operators:
            validate_arithmetic(node.children[i], scope, assign)

    return True


def validate_string(node: Node, scope: SymbolTable, assign: str):
    if node.children[0].type != 'string' and node.children[0].type == '+':
        if not is_string_concat(node, scope):
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "number" to string "' + assign + '".')
            raise NameError('Incompatible declaration.')

    raise_error = False
    for child in node.children:
        if child.type == 'id':
            type_error = search_variable_type(child.value, scope)
            if not type_error in ['string', 'float', 'int']:
                raise_error = True
        elif child.type == '+':
            validate_string_concatenation(child, scope, assign)
        if raise_error:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "' + type_error +'" to string "' + assign + '".')
            raise NameError('Incompatible declaration.')
    return True


def validate_string_concatenation(node: Node, scope: SymbolTable, assign:str, arith_childs=False):
    concat = [node.children[0].value, node.children[1].value]
    child_types = [node.children[0].type, node.children[1].type]

    # Find id types if needed
    for i in range(2):
        if child_types[i] == 'id':
            child_types[i] = search_variable_type(concat[i], scope)

    # Helps to detect when an arithmetic operation is being concatenated
    for i in range(2):
        if not arith_childs:
            if concat[i] in operators:
                arith_childs = not is_string_concat(node.children[i], scope)

    for i in range(2):
        if child_types[i] == 'string':
            pass
        elif not arith_childs:
            if child_types[i] == 'boolean':
                logger.error('[!] Semantic error.')
                logger.info('[?] Can not concatenate a "' + child_types[i] +'" to string "' + assign + '".')
                raise NameError('Incompatible declaration.')
            elif child_types[i] in operators:
                validate_string_concatenation(node.children[i], scope, assign, arith_childs)
        else:
            validate_arithmetic(node.children[i], scope, assign)


def is_string_concat(node: Node, scope: SymbolTable):
    is_concat = False
    for child in node.children:
        if is_concat == True:
            return True

        if child.type == 'string':
            return True
        elif child.type in operators:
            is_concat = is_string_concat(child, scope)
        elif child.type == 'id' and search_variable_type(child.value, scope) == 'string':
            return True
    return is_concat


def validate_boolean(node: Node, scope: SymbolTable, assign: str):
    raise_error = False
    for child in node.children:
        if child.type == 'id':
            type_error = search_variable_type(child.value, scope)
            if type_error != 'boolean':
                raise_error = True
        elif child.type in comparators or child.type in logic_compar:
            validate_compar_types(child, scope)
        if raise_error:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not assign a "' + type_error +'" to boolean "' + assign + '".')
            raise NameError('Incompatible declaration.')
    return True


def validate_compar_types(node: Node, scope: SymbolTable):
    child_types = [None, None]
    for i, child in enumerate(node.children):
        if child.type == 'id':
            child_types[i] = search_variable_type(child.value, scope)
        elif child.type in comparators or child.type in logic_compar:
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
        assign_type = search_variable_type(declare_child.value, table)

        if not assign_type in ['float', 'int']:
            logger.error('[!] Semantic error.')
            logger.info('[?] Can not use "' + assign_type + '" to traverse in a for loop.')
            raise NameError('Incompatible declaration.')
        
        if assign_type == 'int':
            validate_int(declare_child, table, declare_child.value)
    else:
        assign_type = search_variable_type(declare_child.value, table, False)

        if assign_type != None:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable previously defined: ' + str(declare_child.value) + '.')
            raise NameError("The variable " + declare_child.value + " had already been defined.")
        if declare_child.type == 'dint':
            validate_int(declare_child, table, declare_child.value)

        table.children[declare_child.value] = {'type': var_declare[declare_child.type]}
    
    if declare_child.children[0].type in operators:
        validate_arithmetic(declare_child.children[0], table, declare_child.value)

    # Condition
    validate_compar_types(node.children[1], table)
    
    # Instruction
    ins_type = search_variable_type(node.children[3].children[0].value, table)
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
            child_types[i] = search_variable_type(child.value, scope)
        elif child.type in comparators or child.type in logic_compar:
            child_types[i] = validate_compar_types(child, scope)
            comparing = True
        elif child.type in operators:
            if is_string_concat(child, scope):
                validate_string(child, scope, 'Print Statement')
            else:
                validate_arithmetic(child, scope, 'Print Statement')
            # else:
            #     child_types[i] = validate_int(child, scope, 'Print Statement')

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
        analize_semantics(input)
        logger.success('Semantic is correct.')
    except SyntaxError or NameError:
        pass
    
        
