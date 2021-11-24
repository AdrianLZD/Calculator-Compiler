class SymbolTable:

    def __init__(self, id, parent = None, children = {}):
        self.id = id
        self.parent = parent
        self.children = children

    def print(self, offset: str = ''):
        toStr = offset + str(self.id)
        for key, child in self.children.items():
            if type(child) == SymbolTable:
                toStr += offset + '\n' + child.print(offset + '    ')
            else:
                toStr += '\n' + offset + '    ' + key + ': ' + str(child)

        return toStr

    def __str__(self):
        return self.print()

    
