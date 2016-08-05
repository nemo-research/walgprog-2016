import os
import unittest

import codecompare.config as config
from codecompare.ast import ast


class ASTTest(unittest.TestCase):

    def setUp(self):
        self.config = config.Config()
        self.path = os.path.dirname(__file__)

    def testAST_latin1(self):
        self.assertEquals(ast(self.config, open(self.path + os.sep + 'code_latin1.py').read()),
                          ['0 Module', '0  Stmt', '3   Printnl', '3    Const'])

    def testAST_utf8(self):
        self.assertEquals(ast(self.config, open(self.path + os.sep + 'code_utf8.py').read()),
                          ['0 Module', '0  Stmt', '3   Printnl', '3    Const'])

    def testAST_wrong_encode(self):
        try:
            ast(self.config, open(self.path + os.sep + 'code_latin1.py').read().decode('latin1'))
            self.fail("Expecting UnicodeEncodeError")
        except (UnicodeEncodeError):
            pass
