class SymbolTable:

    def __init__(self, id, parent = None, children = {}):
        self.id = id
        self.parent = parent
        self.children = children

    def print(self, offset: str = ''):
        toStr = offset + str(self.id)
        print(self.id)
        for key, child in self.children.items():
            if type(child) == SymbolTable:
                toStr += offset + '\n' + child.print(offset + '    ')
            else:
                
                toStr += offset + '\n' + child.key +': ' + str(child)


        return toStr

    
