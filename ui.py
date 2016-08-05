""" Basic UI handling functions. """

import os
import sys
import getopt

from documents import Document
from ast import ast

def __help(config):
    """ Prints help message. """
    print "Usage:", sys.argv[0], \
            ' '.join(['[--' + op + ']' for op in config.keys()]), \
            '[--sim SIMILARITY_STRATEGY] DIRECTORY'


def get_opts(args, config):
    """
    Parses args using config keys as options.

    @type  args: list
    @param args: args received by sys

    @type  config: Config
    @param config: Configuration object.

    @rtype  str
    @return Directory name passed as argument.
    """
    try:
        longopts = [x for x in config.keys()] + ['sim='] + ['testfile=']
        opts, args = getopt.getopt(args, '', longopts=longopts)
    except getopt.GetoptError, err:
        print "Error:", str(err)
        __help(config)
        sys.exit(2)
    config['sim'] = 'token'
    config['testfile'] = None
    for opt, value in opts:  # pylint: disable=W0612
        if opt == '--help':
            __help(config)
            sys.exit(0)
        elif opt == '--sim':
            config['sim'] = value
        elif opt == '--testfile':
            config['testfile'] = value
        else:
            config[opt[2:]] = True
    if not args:
        print "Missing DIRECTORY/FILES."
        __help(config)
        sys.exit(3)

    invalid = False
    for dirname in args:
        if not os.path.isdir(dirname) and not os.path.isfile(dirname):
            print "Directory/File: " + dirname + " invalid."
            invalid = True
    if invalid:
        __help(config)
        sys.exit(4)
    return args


def read_doc_from_file(config, filename, name=None):
    """ Create a document from file. If pytho source code
    has syntax problems it will return None.

    If acceptempty is enable, it will create (almost) empty documents
    from source files without code (module is always the root node from
    a python AST). """
    if not name:
        name = filename
    o_file = open(filename, 'rb')
    try:
        text = ast(config, o_file.read())
        if not config['acceptempty'] and len(text) <= 2:
            return None
        return Document(name, text)
    except (SyntaxError, UnicodeEncodeError):
        return None
    finally:
        o_file.close()


def read_docs_from_list(config, filelist):
    """ Create a dictionary with documents read from filelist. """
    docs = {}
    for filepath in filelist:
        docs[filepath] = read_doc_from_file(config, filepath)
    return docs
