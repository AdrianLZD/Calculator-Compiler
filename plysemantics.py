import plyparser
import operator
import string
from node import Node
from symboltable import SymbolTable


operators = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '^' : operator.pow
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
    'float' : float
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
    symbol_table = SymbolTable('1', None, {})
    child_blocks = 0
    parse_tree : Node = plyparser.parse_input(input)
    for child in parse_tree.children:
        if child.type in var_declare:
            symbol_table.children[child.value] = {'type' : var_declare[child.type], 'value': evaluate(child.children[0], symbol_table)}

        elif child.type in flowctrls:
            child_blocks += 1
            if child.type == 'if':
                symbol_table.children[child.value] = create_block_table(child.children[0].children[1], symbol_table, child_blocks)

    
    return symbol_table


def create_block_table(node: Node, parent: SymbolTable, id: int):
    child_blocks = 0
    table = SymbolTable(parent.id + "." + str(id), parent, {})
    for child in node.children:
        if child.type in var_declare:
            table.children[child.value] = {'type': var_declare[child.type], 'value': evaluate(child.children[0], table)}

        elif child.type in flowctrls:
            child_blocks += 1
            table.children[child.value] = create_block_table(child, table, child_blocks)

        elif child.type == 'id':
            idData = search_in_parent(child.value, table)
            table.children[child.value] = {'type' :idData[0], 'value': evaluate(child.children[0], table)}

    return table


def evaluate(node: Node, scope : SymbolTable):
    if node.type in operators:
        return operators[node.type]( 
            evaluate(node.children[0], scope), 
            evaluate(node.children[1], scope) )
    elif node.type in var_types:
        return node.value
    elif node.type == 'id':
        if node.value in scope.children:
            valType = scope.children[node.value]['type']
            if valType == 'boolean' or valType == 'string':
                return scope.children[node.value]['value']
            else:
                return var_cast[valType](scope.children[node.value]['value'])
        else:
            return search_in_parent(node.value, scope.parent)[1]
        

def search_in_parent(id : string, parent: SymbolTable):
    if id in parent.children:
        valType = parent.children[id]['type']
        if valType == 'boolean' or valType == 'string':
            return [parent.children[id]['type'], parent.children[id]['value']]
        else:
            return [parent.children[id]['type'], var_cast[valType](parent.children[id]['value'])]
    elif parent.parent != None:
        return search_in_parent(id, parent.parent)
    else:
        raise NameError("Can not reference a variable not previously defined: " + id)


if __name__ == '__main__':
    input = file_to_str('testing/input_files/basic.txt')
    try:
        create_symbols_table(input)
    except NameError as e:
        print(e)
        
