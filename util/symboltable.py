class SymbolTable:

    def __init__(self, id, parent = None, children = {}, block_childs = 0):
        self.id = id
        self.parent = parent
        self.children = children
        self.block_childs = block_childs

    def print(self, offset: str = '', key: str = ''):
        if key != '':
            toStr = offset + str(key) + ':' + str(self.id)
        else:
            toStr = offset + str(self.id)
        for key, child in self.children.items():
            if type(child) == SymbolTable:
                toStr += offset + '\n' + child.print(offset + '    ', key)
            else:
                toStr += '\n' + offset + '    ' + key + ': ' + str(child)

        return toStr

    def find(self, id):
        if id in self.children:
            return self.children[id]
        
        if self.parent != None:
            return self.parent.find(id)

        return None
                

    def __str__(self):
        return self.print()

    
