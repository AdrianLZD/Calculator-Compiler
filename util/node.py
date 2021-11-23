class Node:
    def __init__(self, type, value, children=[], parent=None):
        self.type = type
        self.value = value
        self.children = children
        self.parent = parent

    def print(self, offset: str = ''):
        toStr = offset + 't: ' + str(self.type) + '\n'

        if type(self.value) == Node:
            toStr += offset + 'v:\n' + self.value.print(offset + '    ') + '\n'
        else:
            toStr += offset + 'v: ' + str(self.value) + '\n'

        hasChilds = False
        for i, child in enumerate(self.children):
            if i == 0:
                toStr += offset + 'c:\n' + child.print(offset + '    ')
            else:
                toStr += '\n' + offset + '    -----'
                toStr += offset + '\n' + child.print(offset + '    ')
            
            hasChilds = True
        if not hasChilds:
            toStr += offset + 'c:'

        if self.parent == None:
            toStr += '\n' + offset + 'p: ' + str(self.parent)

        return toStr


    def __str__(self):
        return self.print()


    # Prints only the value of nodes
    def print_basic_test(self):
        toStr = ''
        if type(self.value) == Node:
            toStr += self.type + '|'
            toStr += self.value.print_basic_test()
        else:
            toStr += str(self.value) + '|'
            
        for child in self.children:
            toStr += child.print_basic_test()

        return toStr

    # Prints value and parent of nodes
    def print_parent_test(self, depth = 0):
        toStr = ''
        if type(self.value) == Node:
            toStr += 'P' + str(depth) + '_'
            toStr += self.type + '|'
            toStr += self.value.print_parent_test(depth=depth+1)
        else:
            toStr += 'P' + str(depth) + '_'
            toStr += str(self.value) + '|'

        for child in self.children:
            toStr += child.print_parent_test(depth=depth+1)

        return toStr
