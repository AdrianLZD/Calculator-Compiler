import plysemantics
from util.node import Node
from plysemantics import var_declare, var_types, operators, comparators

def gen():
    n = 0
    while(True):
        yield n
        n += 1
        

var_id = gen()

code = ''

logic_compar = {
    'or' : 'or',
    'and' : 'and'
}

def generate_code(file):
    input = plysemantics.file_to_str(file)
    semantics = plysemantics.analize_semantics(input)
    abs_tree = semantics[0]
    sym_table = semantics[1]
    print(abs_tree)
    analize_tree(abs_tree, sym_table)


def analize_tree(tree, table):
    convert_node(tree)


def convert_node(node: Node):
    for child in node.children:
        if child.type in var_declare:
            add_to_code([child.value,'=', convert_instruction(child.children[0])])


def convert_instruction(node: Node):
    if node.type in var_types:
        return node.value
    elif node.type in operators:
        if node.parent.type in ['dstring', 'string']:
            return concat_strings(node)
        else:
            return arithmetic_operation(node, node.parent.type == 'dfloat')
    elif node.type in logic_compar or node.type in comparators:
        return boolean_operation(node)


def arithmetic_operation(node: Node, isFloatOperation: bool = False):
    operate = [node.children[0].value, node.children[1].value]
    for i in range(2):
        if node.children[i].type == 'float':
            isFloatOperation = True

    for i in range(2):
        if isFloatOperation and node.children[i].type == 'int':
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toFloat', node.children[i].value])
            operate[i] = 't' + str(var_num)
        if node.children[i].type in operators:
            operate[i] = arithmetic_operation(node.children[i], isFloatOperation)
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', operate[0], node.value, operate[1]])
    return 't' + str(var_num)


def concat_strings(node: Node):
    concat = [node.children[0].value, node.children[1].value]
    for i in range(2):
        if node.children[i].type in ['int', 'float']:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toString', node.children[i].value])
            concat[i] = 't' + str(var_num)
        elif node.children[i].type in operators:
            concat[i] = concat_strings(node.children[i])
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', concat[0], '+', concat[1]])
    return 't' + str(var_num)


def boolean_operation(node: Node):
    evaluate = [node.children[0].value, node.children[1].value]
    for i in range(2):
        if node.children[i].type in ['int', 'float']:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', node.children[i].value])
            evaluate[i] = 't' + str(var_num)
        
        if node.children[i].type in logic_compar or node.children[i].type in comparators:
            evaluate[i] = boolean_operation(node.children[i])
        elif node.children[i].type in operators:
            arithmetic = arithmetic_operation(node.children[i])
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', arithmetic])
            evaluate[i] = 't' + str(var_num)

    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', evaluate[0], node.value, evaluate[1]])
    return 't' + str(var_num)


def add_to_code(values):
    global code
    for val in values:
        code += str(val) + " "
    code += "\n"


if __name__ == '__main__':
    generate_code('input/basic.txt')
    print(code)
