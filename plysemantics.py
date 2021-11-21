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
    'if' : 'if'
}


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
        symbol_table = create_block_table(parse_tree, symbol_table, 1)
    except NameError as e:
        pass
    return symbol_table


def create_block_table(node: Node, parent: SymbolTable, id: int):
    child_blocks = 0
    id_prefix = parent.id + '.' if parent.id != '' else parent.id
    table = SymbolTable(id_prefix + str(id), parent, {})
    for child in node.children:
        if child.type in var_declare:
            available = False
            if not (child.value in table.children) or search_in_parent(child.value, parent, False) == None:
                available = True

            if available == True:
                table.children[child.value] = {'type': var_declare[child.type], 'value': evaluate(child.children[0], table)}
            else:
                logger.error('[!] Semantic error.')
                logger.info('[?] Variable previously defined: ' + str(child.value) + '.')
                raise NameError("The variable " + child.value + " had already been defined.")

        elif child.type in flowctrls:
            child_blocks += 1
            if child.type == 'if':
                table.children[child.value] = evaluate_if(child, table, child_blocks)
                
        elif child.type == 'id':
            idData = search_in_parent(child.value, table)
            table.children[child.value] = {'type' :idData[0], 'value': evaluate(child.children[0], table)}

    return table

# Evaluates an instruction
def evaluate(node: Node, scope : SymbolTable):
    if node.type in operators:
        return operators[node.type]( 
            evaluate(node.children[0], scope), 
            evaluate(node.children[1], scope) )

    elif node.type in var_types:
        return var_cast[node.type](node.value)

    elif node.type == 'id':
        if node.value in scope.children:
            valType = scope.children[node.value]['type']
            if valType == 'boolean' or valType == 'string':
                return scope.children[node.value]['value']
            else:
                return var_cast[valType](scope.children[node.value]['value'])
        else:
            return search_in_parent(node.value, scope.parent)[1]

    elif node.type == 'cond':
        return evaluate(node.children[0], scope)

    elif node.type in comparators:
        childs = {}
        for i,child in enumerate(node.children):
            if child.type == 'id':
                nodeData = search_in_parent(child.value, scope)
                childs[i] = Node(nodeData[0], nodeData[1])
            else:
                childs[i] = child

        if childs[0].type in ['boolean', 'string'] or childs[1].type in ['boolean', 'string']:
            logger.error('[!] Semantic error.')
            logger.info('[?] Comparison "' + node.type + '" not supported between "' + childs[0].type + '" and "' + childs[1].type + '".')
            raise NameError("The variable " + child.value + " had already been defined.")

        return comparators[node.type](
            evaluate(childs[0], scope),
            evaluate(childs[1], scope) )


# Retrieves the type and value of a variable
def search_in_parent(id : string, parent: SymbolTable, raiseException = True):
    if id in parent.children:
        valType = parent.children[id]['type']
        if valType == 'boolean' or valType == 'string':
            return [parent.children[id]['type'], parent.children[id]['value']]
        else:
            return [parent.children[id]['type'], var_cast[valType](parent.children[id]['value'])]
    elif parent.parent != None:
        return search_in_parent(id, parent.parent)
    else:
        if raiseException == True:
            logger.error('[!] Semantic error.')
            logger.info('[?] Variable not defined: ' + id + '.')
            raise NameError("Can not reference a variable not previously defined: " + id + '.')
        else:
            return None


def evaluate_if(node: Node, parent: SymbolTable, blocks: int):
    for child in node.children:
        if child.type == 'else':
            return create_block_table(child.children[0], parent, blocks)
        elif evaluate(child, parent):
            return create_block_table(child.children[1], parent, blocks)


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
    
        
