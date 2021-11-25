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


def generate_code(file):
    input = plysemantics.file_to_str(file)
    semantics = plysemantics.analize_semantics(input)
    abs_tree = semantics[0]
    sym_table = semantics[1]
    print(abs_tree)
    print(sym_table)
    analize_tree(abs_tree, sym_table)


def analize_tree(tree, scope):
    convert_node(tree, scope)


def convert_node(node: Node, scope: SymbolTable, block_count = 0):
    for child in node.children:
        if child.type in var_declare:
            add_to_code([child.value,'=', convert_instruction(child.children[0], scope, block_count)])
        elif child.type == 'id':
            convert_id_declaration(child, scope, block_count)
        elif child.type in flowctrls:
            if child.type == 'if':
                block_count = conditional_block(child, scope, block_count)
            elif child.type == 'while':
                block_count = while_instruction(child, scope, block_count)
            elif child.type == 'for':
                block_count = for_instruction(child, scope, block_count)
        


def convert_instruction(node: Node, scope: SymbolTable, block_count: int):
    if node.type in var_types:
        return node.value
    elif node.type in operators:
        if node.parent.type in ['dstring', 'string']:
            return concat_strings(node, scope, block_count)
        else:
            return arithmetic_operation(node, scope, node.parent.type == 'dfloat')
    elif node.type in logic_compar or node.type in comparators:
        return boolean_operation(node, scope, block_count)


def arithmetic_operation(node: Node, scope: SymbolTable, block_count: int,  is_float_operation: bool = False):
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
            operate[i] = arithmetic_operation(node.children[i],scope, is_float_operation)
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', operate[0], node.value, operate[1]])
    return 't' + str(var_num)


def concat_strings(node: Node, scope: SymbolTable, block_count: int):
    concat = [node.children[0].value, node.children[1].value]
    for i in range(2):
        if node.children[i].type in ['int', 'float']:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toString', node.children[i].value])
            concat[i] = 't' + str(var_num)
        elif node.children[i].type in operators:
            concat[i] = concat_strings(node.children[i], scope, block_count)
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', concat[0], '+', concat[1]])
    return 't' + str(var_num)


def boolean_operation(node: Node, scope: SymbolTable, block_count: int):
    evaluate = [node.children[0].value, node.children[1].value]
    for i in range(2):
        if node.children[i].type in ['int', 'float', 'string'] and node.children[i].type in logic_compar:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', node.children[i].value])
            evaluate[i] = 't' + str(var_num)
        
        if node.children[i].type in logic_compar or node.children[i].type in comparators:
            evaluate[i] = boolean_operation(node.children[i], scope, block_count)
        elif node.children[i].type in operators:
            arithmetic = arithmetic_operation(node.children[i], scope, block_count)
            if node.type in logic_compar:
                var_num = next(var_id)
                add_to_code(['t' + str(var_num), '=', 'toBoolean', arithmetic])
                evaluate[i] = 't' + str(var_num)
            else:
                evaluate[i] = arithmetic

    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', evaluate[0], node.value, evaluate[1]])
    return 't' + str(var_num)


def convert_id_declaration(node: Node, scope: SymbolTable, block_count: int):
    id_data = scope.find(node.value)
    if id_data['type'] in ['int', 'float']:
        add_to_code([node.value, '=', convert_instruction(node.children[0], scope, block_count)])
    elif id_data['type'] == 'string':
        if node.children[0].type == 'string':
            add_to_code([node.value, '=', convert_instruction(node.children[0].value, scope, block_count)])
        else:
            add_to_code([node.value, '=', concat_strings(node.children[0], scope, block_count)])
    elif id_data['type'] == 'boolean':
        add_to_code([node.value, '=', boolean_operation(node.children[0], scope, block_count)])


def conditional_block(node: Node, scope: SymbolTable, block_count: int, add_else_ref_to_code: bool = True):
    blocks_ref = []
    has_else = False
    for child in node.children:
        if child.type == 'else':
            condition = 'True'
            has_else = True
        elif child.children[0].type in ['int', 'float', 'string']:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', child.children[0].value])
            condition = 't' + str(var_num)
        elif child.children[0].type == 'boolean':
            condition = child.children[0].value
        else:
            condition = boolean_operation(node.children[0].children[0], scope, block_count)  
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

    for i, child in enumerate(node.children):
        add_to_code([blocks_ref[i]])
        if child.type == 'else':
            convert_node(child.children[0], scope.children[node.type + str(i + block_count)], 0)
        else:
            convert_node(child.children[1], scope.children[node.type + str(i + block_count)], 0)

    if not has_else and add_else_ref_to_code:
        add_to_code([blocks_ref[len(blocks_ref)-1]])

    return len(node.children) + block_count


def while_instruction(node: Node, scope: SymbolTable, block_count: int):
    block_num = next(block_id)
    add_to_code(['L' + str(block_num)])
    block_count = conditional_block(node, scope, block_count, False)
    add_to_code(['True', 'IFGOTO' ,'L' + str(block_num)])
    add_to_code(['L' + str(block_num + 2)])
    return block_count


def for_instruction(node: Node, scope: SymbolTable, block_count: int):
    # Declare variable to iterate
    for_instruction_declaration(node.children[0], scope, block_count)
    # Create reference to reevaluate condition
    block_num = next(block_id)
    add_to_code(['L'+str(block_num)])
    # Convert the condition to actual code
    for_instruction_condition(node.children[1], scope, block_count)
    # Create the block to iterate over
    add_to_code(['L'+str(block_num + 1)])
    convert_node(node.children[2], scope.children['for' + str(block_count)], 0)
    # Declare the instruction to do after each iteration
    add_to_code([node.children[0].value, '=', node.children[0].value, node.children[3].value, '1'])
    # Return to evaluate the condition
    add_to_code(['True', 'IFGOTO', 'L'+str(block_num)])
    # Exit for
    add_to_code(['L'+str(block_num + 2)])



    
def for_instruction_declaration(node: Node, scope: SymbolTable, block_count: int):
    if node.type in var_declare:
        add_to_code([node.value, '=', convert_instruction(node.children[0], scope, block_count)])
    else:
        convert_id_declaration(node, scope, block_count)


def for_instruction_condition(node: Node, scope: SymbolTable, block_count: int):
    if node.children[0].type in ['int', 'float', 'string']:
        var_num = next(var_id)
        add_to_code(['t' + str(var_num), '=', 'toBoolean', node.children[0].value])
    elif node.children[0].type == 'boolean':
        var_num = next(var_id)
        add_to_code(['t' + str(var_num), '=', node.children[0].value])
    else:
        condition_value = boolean_operation(node.children[0], scope.children['for' + str(block_count)], block_count)
        cond_num = next(cond_id)
        block_num = next(block_id)
        condition_id = 'v' + str(cond_num)
        add_to_code([condition_id, '=', condition_value])
        add_to_code([condition_id, 'IFGOTO', 'L' + str(block_num)])

    cond_num = next(cond_id)
    block_num = next(block_id)
    condition = 'True'
    condition_id = 'v' + str(cond_num)
    add_to_code([condition_id, '=', condition])
    add_to_code([condition_id, 'IFGOTO', 'L' + str(block_num)])

    


def add_to_code(values):
    global code
    for val in values:
        code += str(val) + " "
    code += "\n"


if __name__ == '__main__':
    generate_code('input/basic.txt')
    print(code)
