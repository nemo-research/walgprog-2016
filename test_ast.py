import unittest

import codecompare.config
from codecompare.ast import ast


class ASTTest(unittest.TestCase):

    def setUp(self):
        self.config = codecompare.config.Config()
        self.code = "def fun(something):\n    return something > 2\na = 1\nprint fun(a)\nassert a\na.value()"
        self.maxDiff = None

    def testAST(self):
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name', '2       Const',
                           '3   Assign', '3    AssName', '3    Const',
                           '4   Printnl', '4    CallFunc fun', '4     Name', '4     Name',
                           '5   Assert', '5    Name',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name'])

    def testASTNoIdent(self):
        self.assertFalse(self.config['no_ident'])
        self.config['no_ident'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0 Stmt',
                           '1 Function', '1 Stmt',
                           '2 Return', '2 Compare >', '2 Name', '2 Const',
                           '3 Assign', '3 AssName', '3 Const',
                           '4 Printnl', '4 CallFunc fun', '4 Name', '4 Name',
                           '5 Assert', '5 Name',
                           '6 Discard', '6 CallFunc', '6 Getattr value', '6 Name'])

    def testASTNoAsserts(self):
        self.assertFalse(self.config['no_asserts'])
        self.config['no_asserts'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name', '2       Const',
                           '3   Assign', '3    AssName', '3    Const',
                           '4   Printnl', '4    CallFunc fun', '4     Name', '4     Name',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name'])

    def testASTNoIgnorePrimitives(self):
        self.assertFalse(self.config['no_ignore_primitives'])
        self.config['no_ignore_primitives'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name', '2       Const 2',
                           '3   Assign', '3    AssName', '3    Const 1',
                           '4   Printnl', '4    CallFunc fun', '4     Name', '4     Name',
                           '5   Assert', '5    Name',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name'])

    def testASTNoAnonymize(self):
        self.assertFalse(self.config['no_anonymize'])
        self.config['no_anonymize'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    fun', '1    [\'something\']', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name something', '2        something', '2       >', '2       Const', '2        2',
                           '3   Assign', '3    AssName', '3     a', '3     OP_ASSIGN', '3    Const', '3     1',
                           '4   Printnl', '4    CallFunc fun', '4     Name fun', '4      fun', '4     Name a', '4      a',
                           '5   Assert', '5    Name a', '5     a',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name a', '6       a', '6      value'])

    def testASTNoGetAttr(self):
        self.assertFalse(self.config['no_getattr'])
        self.config['no_getattr'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name', '2       Const',
                           '3   Assign', '3    AssName', '3    Const',
                           '4   Printnl', '4    CallFunc fun', '4     Name', '4     Name',
                           '5   Assert', '5    Name',
                           '6   Discard', '6    CallFunc', '6     Getattr', '6      Name'])

    def testASTNoCompare(self):
        self.assertFalse(self.config['no_compare'])
        self.config['no_compare'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare', '2       Name', '2       Const',
                           '3   Assign', '3    AssName', '3    Const',
                           '4   Printnl', '4    CallFunc fun', '4     Name', '4     Name',
                           '5   Assert', '5    Name',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name'])

    def testASTNoCallFunc(self):
        self.assertFalse(self.config['no_callfunc'])
        self.config['no_callfunc'] = True
        self.assertEquals(ast(self.config, self.code),
                          ['0 Module', '0  Stmt',
                           '1   Function', '1    Stmt',
                           '2     Return', '2      Compare >', '2       Name', '2       Const',
                           '3   Assign', '3    AssName', '3    Const',
                           '4   Printnl', '4    CallFunc', '4     Name', '4     Name',
                           '5   Assert', '5    Name',
                           '6   Discard', '6    CallFunc', '6     Getattr value', '6      Name'])

    def testEmptyAST(self):
        self.assertEquals(ast(self.config, ''), ['0 Module', '0  Stmt'])
