import plysemantics



def generate_code(file):
    input = plysemantics.file_to_str(file)
    semantics = plysemantics.analize_semantics(input)
    abs_tree = semantics[0]
    sym_table = semantics[1]
    analize_tree(abs_tree, sym_table)

def analize_tree(tree, table):
    print(tree)
    pass



if __name__ == '__main__':
    generate_code('input/basic.txt')
