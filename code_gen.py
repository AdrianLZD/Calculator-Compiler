import plysemantics
from util.node import Node
from plysemantics import var_declare, var_types, operators, flowctrls
from util.symboltable import SymbolTable

def gen():
    n = 0
    while(True):
        yield n
        n += 1
        

var_id = gen()
block_id = gen()
cond_id = gen()

code = ''

logic_compar = {
    'or' : 'or',
    'and' : 'and'
}

comparators = dict(plysemantics.comparators)
comparators.update({
    '==': '==',
    '!=': '!='
})

sym_table = {}

def generate_code(file):
    input = plysemantics.file_to_str(file)
    semantics = plysemantics.analize_semantics(input)
    abs_tree = semantics[0]
    global sym_table
    sym_table = semantics[1]
    print(abs_tree)
    analize_tree(abs_tree)


def analize_tree(tree):
    convert_node(tree)


def convert_node(node: Node):
    for child in node.children:
        if child.type in var_declare:
            add_to_code([child.value,'=', convert_instruction(child.children[0])])
        elif child.type == 'id':
            convert_id_declaration(child)
        elif child.type in flowctrls:
            if child.type == 'if':
                if_instruction(child)
        


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


def arithmetic_operation(node: Node, is_float_operation: bool = False):
    operate = [node.children[0].value, node.children[1].value]
    if not is_float_operation:
        for i in range(2):
            if node.children[i].type == 'float':
                is_float_operation = True

    for i in range(2):
        if is_float_operation and node.children[i].type == 'int':
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toFloat', node.children[i].value])
            operate[i] = 't' + str(var_num)
        if node.children[i].type in operators:
            operate[i] = arithmetic_operation(node.children[i], is_float_operation)
        
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
        if node.children[i].type in ['int', 'float', 'string'] and node.children[i].type in logic_compar:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', node.children[i].value])
            evaluate[i] = 't' + str(var_num)
        
        if node.children[i].type in logic_compar or node.children[i].type in comparators:
            evaluate[i] = boolean_operation(node.children[i])
        elif node.children[i].type in operators:
            arithmetic = arithmetic_operation(node.children[i])
            if node.children[i].type in logic_compar:
                var_num = next(var_id)
                add_to_code(['t' + str(var_num), '=', 'toBoolean', arithmetic])
                evaluate[i] = 't' + str(var_num)
            else:
                evaluate[i] = arithmetic

    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', evaluate[0], node.value, evaluate[1]])
    return 't' + str(var_num)


def convert_id_declaration(node: Node):
    global sym_table
    id_data = sym_table.find(node.value)
    if id_data['type'] in ['int', 'float']:
        add_to_code([node.value, '=', convert_instruction(node.children[0])])
    elif id_data['type'] == 'string':
        if node.children[0].type == 'string':
            add_to_code([node.value, '=', convert_instruction(node.children[0].value)])
        else:
            add_to_code([node.value, '=', concat_strings(node.children[0])])
    elif id_data['type'] == 'boolean':
        add_to_code([node.value, '=', boolean_operation(node.children[0])])


def if_instruction(node: Node):
    blocks_ref = []
    has_else = False
    for child in node.children:
        if child.type == 'else':
            condition = 'True'
            has_else = True
        else:
            condition = boolean_operation(node.children[0].children[0])
        cond_num = next(cond_id)
        block_num = next(block_id)
        condition_id = 'v' + str(cond_num)
        add_to_code([condition_id, '=', condition])
        add_to_code([condition_id, 'IFGOTO', 'L' + str(block_num)])
        blocks_ref.append('L' + str(block_num))
        
    if not has_else:
        cond_num = next(cond_id)
        block_num = next(block_id)
        condition = 'True'
        condition_id = 'v' + str(cond_num)
        add_to_code([condition_id, '=', condition])
        add_to_code([condition_id, 'IFGOTO', 'L' + str(block_num)])
        blocks_ref.append('L' + str(block_num))

    block_index = 0
    for child in node.children:
        add_to_code([blocks_ref[block_index]])
        block_index += 1
        convert_node(node.children[0].children[1])

    if not has_else:
        add_to_code([blocks_ref[len(blocks_ref)-1]])


def add_to_code(values):
    global code
    for val in values:
        code += str(val) + " "
    code += "\n"


if __name__ == '__main__':
    generate_code('input/basic.txt')
    print(code)
