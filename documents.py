""" Module to hold data structures to be used on codecompare. """

class Document:  # pylint: disable=R0903
    """ An user submission. """

    def __init__(self, name, text):
        self.name = name
        self.nodes = _DocumentNodes()  # AST node
        self.lines_no = {}
        for line in text:
            lineno, line = line.split(' ', 1)  # LINENO AST_NODE_INFO
            self.nodes.append(line)
            lineno_list = self.lines_no.get(line, [])
            lineno_list.append(lineno)

    def __hash__(self):
        return hash(self.name)

class _DocumentNodes(list):

    def hash(self):
        return hash(tuple(self))