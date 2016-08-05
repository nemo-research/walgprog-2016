"""
Handles AST processing.

Based upon: http://code.activestate.com/recipes/533146-ast-pretty-printer/
"""

import compiler
from compiler.ast import Node
from compiler import parse


def ast(config, code):
    """
    Call AST to compile code in text format (one node per line).

    @type  config: Config
    @param config: Configuration dict settings.

    @type  code: str
    @param code: Filename of source code.

    @rtype: list
    @returns AST in a list:
    """
    # from: http://nullege.com/codes/show/src%40r%40e%40RestrictedPython-3.6.0%40src%40RestrictedPython%40RCompile.py/19/compiler.parse/python
    #  code = '\xef\xbb\xbf' + code.encode('utf-8')
    parsed_ast = parse(code)
    text = ['']
    __rec_node(config, parsed_ast, 0, text, 0)
    text.pop()  # Remove last add
    return text


def __rec_identation(config, level):
    """ Considers identation (depth) """
    return '' if config['no_ident'] else ' ' * level


def __rec_lineno(node, lineno):
    """ Records line number associated with parsed code """
    return str(node.lineno) + ' ' if hasattr(node, 'lineno') and node.lineno else str(lineno) + ' '


def __rec_names(config, node):
    """ Records names used. """
    return ' ' + node.name if config['no_anonymize'] else ''


def __rec_getattr(config, node):
    """ Record attributes used. """
    return '' if config['no_getattr'] else ' ' + node.attrname


# pylint: disable=R0913
def __rec_node(config, node, level, text, lineno):
    """ Recursive magic to parse AST. """
    pfx = __rec_lineno(node, lineno)
    pfx += __rec_identation(config, level)

    if not isinstance(node, Node):  # Leafs
        if not config['no_anonymize'] and (isinstance(node, tuple) or isinstance(node, list)):
            return
        elif node and config['no_anonymize']:
            text[-1] += str(pfx)
            text[-1] += str(node)
            text.append('')
        return

    text[-1] += pfx
    text[-1] += str(node.__class__.__name__)

    if hasattr(node, 'attrname'):
        text[-1] += __rec_getattr(config, node)
    elif isinstance(node, compiler.ast.Name):
        text[-1] += __rec_names(config, node)

    if isinstance(node, compiler.ast.Compare):
        if not config['no_compare']:
            text[-1] += ' ' + node.getChildren()[1]

    if isinstance(node, compiler.ast.Const) and config['no_ignore_primitives']:
        text[-1] += ' ' + str(node.value)

    if isinstance(node, compiler.ast.CallFunc):
        if hasattr(node.node, 'name'):
            if not config['no_callfunc']:
                text[-1] += ' ' + str(node.node.name)

    text.append('')  # Create a new line to be appended latter

    for child in node.getChildren():
        if config['no_asserts'] \
                and isinstance(child, compiler.ast.Assert):
            continue
        lineno = child.lineno if hasattr(child, 'lineno') \
            and child.lineno else lineno
        __rec_node(config, child, level + 1, text, lineno)
