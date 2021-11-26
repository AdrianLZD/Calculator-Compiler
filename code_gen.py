import plysemantics
import sys
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
    #print(abs_tree)
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
        if child.type == 'if':
            block_count = conditional_block(child, scope, block_count)
        elif child.type == 'while':
            block_count = while_instruction(child, scope, block_count)
        elif child.type == 'for':
            block_count = for_instruction(child, scope, block_count)
        elif child.type == 'print':
            print_instruction(child, scope, block_count)
            

def convert_instruction(node: Node, scope: SymbolTable, block_count: int):
    if node.type in var_types:
        if node.parent.type in ['dfloat', 'float'] and node.type == 'int':
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toFloat', node.value])
            return 't' + str(var_num)

        if node.type == 'string':
            quotations = '"'
            if '"' in node.value:
                quotations = "'"
            return quotations + node.value + quotations
        
        return node.value
    elif node.type in operators:
        if node.parent.type in ['dstring', 'string'] or (node.parent.type == 'id' and scope.find(node.parent.value)['type'] == 'string'):
            return concat_strings(node, scope, block_count)
        else:
            id_float_check = False
            if node.parent.type == 'id':
                id_float_check = scope.find(node.parent.value)['type']
            return arithmetic_operation(node, scope, block_count, node.parent.type == 'dfloat' or id_float_check == 'float')
    elif node.type in logic_compar or node.type in comparators:
        return boolean_operation(node, scope, block_count)
    elif node.type == 'id':
        return node.value


def arithmetic_operation(node: Node, scope: SymbolTable, block_count: int,  float_operation: bool = False):
    operate = [node.children[0].value, node.children[1].value]
    child_types = [node.children[0].type, node.children[1].type]

    # Find id types if needed
    for i in range(2):
        if child_types[i] == 'id':
            child_types[i] = scope.find(operate[i])['type']

    # Helps to detect when integers should be casted to floats
    for i in range(2):
        if not float_operation:
            if child_types[i] == 'float':
                float_operation = True
            elif child_types[i] in operators:
                float_operation = is_float_operation(node.children[i], scope)

    for i in range(2):
        if float_operation and child_types[i] == 'int':
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toFloat', operate[i]])
            operate[i] = 't' + str(var_num)
        if child_types[i] in operators:
            operate[i] = arithmetic_operation(node.children[i],scope, block_count, float_operation)
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', operate[0], node.value, operate[1]])
    return 't' + str(var_num)


def concat_strings(node: Node, scope: SymbolTable, block_count: int, arith_childs = False):
    concat = [node.children[0].value, node.children[1].value]
    child_types = [node.children[0].type, node.children[1].type]

    # Find id types if needed
    for i in range(2):
        if child_types[i] == 'id':
            child_types[i] = scope.find(concat[i])['type']

    # Helps to detect when an arithmetic operation is being concatenated
    for i in range(2):
        if not arith_childs:
            if concat[i] in operators:
                arith_childs = not is_string_concat(node.children[i], scope)

    for i in range(2):
        if child_types[i] == 'string' and node.children[i].type != 'id':
            if '"' in concat[i]:
                concat[i] = "'" + concat[i] + "'"
            else:
                concat[i] = '"' + concat[i] + '"'
        elif not arith_childs:
            if child_types[i] in ['int', 'float']:
                var_num = next(var_id)
                add_to_code(['t' + str(var_num), '=', 'toString', concat[i]])
                concat[i] = 't' + str(var_num)
            elif child_types[i] == 'string' and node.children[i].type != 'id':
                if '"' in concat[i]:
                    concat[i] = "'" + concat[i] + "'"
                else:
                    concat[i] = '"' + concat[i] + '"'
            elif child_types[i] in operators:
                concat[i] = concat_strings(node.children[i], scope, block_count, arith_childs)
        else:
            concat[i] = arithmetic_operation(node.children[i], scope, block_count)
            add_to_code([concat[i], '=', 'toString', concat[i]])
        
    var_num = next(var_id)
    add_to_code(['t' + str(var_num), '=', concat[0], '+', concat[1]])
    return 't' + str(var_num)


def boolean_operation(node: Node, scope: SymbolTable, block_count: int, float_compare: bool = False):
    evaluate = [node.children[0].value, node.children[1].value]
    child_types = [node.children[0].type, node.children[1].type]

    # Find id types if needed
    for i in range(2):
        if child_types[i] == 'id':
            child_types[i] = scope.find(evaluate[i])['type']

    # Helps to detect when integers should be casted to floats
    for i in range(2):
        if not float_compare:
            if evaluate[i] in operators:
                float_compare = is_float_operation(node.children[i], scope)
            if child_types[i] == 'float':
                float_compare = True

    for i in range(2):
        # When comparing float, cast integers
        if child_types[i] == 'int' and float_compare:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toFloat', evaluate[i]])
            evaluate[i] = 't' + str(var_num)

        # Make sure the casting to boolean is done if needed
        if child_types[i] in ['int', 'float'] and node.type in logic_compar:
            var_num = next(var_id)
            add_to_code(['t' + str(var_num), '=', 'toBoolean', evaluate[i]])
            evaluate[i] = 't' + str(var_num)

        # Make sure to cast strings if needed
        if child_types[i] == 'string' and node.type in comparators:
            var_num = next(var_id)
            new_var = 't' + str(var_num)
            quotations = '"'
            if '"' in evaluate[i]:
                quotations = "'"
            add_to_code([new_var, '=', 'toBoolean', quotations + evaluate[i] + quotations])
            if float_compare:
                add_to_code([new_var, '=', 'toFloat', new_var])
            else:
                add_to_code([new_var, '=', 'toInt', new_var])
            
            evaluate[i] = new_var

        # Make sure the casting to int is done if needed
        if child_types[i] == 'boolean' and node.type in comparators:
            var_num = next(var_id)
            if float_compare:
                add_to_code(['t' + str(var_num), '=', 'toFloat', evaluate[i]])
            else:
                add_to_code(['t' + str(var_num), '=', 'toInt', evaluate[i]])
            evaluate[i] = 't' + str(var_num)
        
        if child_types[i] in logic_compar or child_types[i] in comparators:
            evaluate[i] = boolean_operation(node.children[i], scope, block_count)
        elif child_types[i] in operators:
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
            add_to_code([node.value, '=', convert_instruction(node.children[0], scope, block_count)])
    elif id_data['type'] == 'boolean':
        add_to_code([node.value, '=', convert_instruction(node.children[0], scope, block_count)])


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
            print(node.type)
            print(i)
            print(block_count)
            convert_node(child.children[1], scope.children[node.type + str(i + block_count)], 0)
            print("done")

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
    return block_count + 1


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


def print_instruction(node: Node, scope: SymbolTable, block_count: int):
    for child in node.children:
        if child.type in var_types:
            add_to_code(['PRINT', child.value])
        elif child.type in operators:
            if child.type == '+' and is_string_concat(child, scope):
                var_print = concat_strings(child, scope, block_count)
            else:
                var_print = arithmetic_operation(child, scope, block_count)
            add_to_code(['PRINT', var_print])
        elif child.type in comparators or child.type in logic_compar:
            var_print = boolean_operation(child, scope, block_count)
            add_to_code(['PRINT', var_print])


def is_string_concat(node: Node, scope: SymbolTable):
    is_concat = False
    for child in node.children:
        if is_concat == True:
            return True

        if child.type == 'string':
            return True
        elif child.type in operators:
            is_concat = is_string_concat(child, scope)
        elif child.type == 'id' and scope.find(child.value)['type'] == 'string':
            return True
    return is_concat


def is_float_operation(node: Node, scope: SymbolTable):
    is_float = False
    for child in node.children:
        if is_float == True:
            return True

        if child.type == 'float':
            return True
        elif child.type in operators:
            is_float = is_float_operation(child, scope)
        elif child.type == 'id' and scope.find(child.value)['type'] == 'float':
            return True
    return is_float


def add_to_code(values):
    global code
    for val in values:
        code += str(val) + " "
    code += "\n"


if __name__ == '__main__':
    args = sys.argv[1:]
    
    generate_code(args[0])
    dirs = args[0].split('/')
    file_name = dirs[len(dirs)-1]
    with open('output/' + file_name, 'w') as f:
        f.write(code)
    print(code)
