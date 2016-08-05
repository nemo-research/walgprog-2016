import copy
import unittest

import codecompare.nj


class DocumentMock:

    def __init__(self, name):
        self.name = name


class NJTest(unittest.TestCase):

    def _v_dict(self, res, exp):
        self.assertEquals(sorted(res.keys()), sorted(exp.keys()))
        for k, v in res.items():
            s_v = sorted(v)
            s_ev = sorted(exp[k])
            self.assertEquals(s_v, s_ev)

    def setUp(self):
        self.A = [[0, 2, 1, 2, 3], [2, 0, 3, 1, 2], [1, 3, 0, 2, 1], [2, 1, 2, 0, 2], [3, 2, 1, 2, 0]]
        self.otus = ["A", "B", "C", 'D', 'E']

    def testNJMatrix(self):
        res = codecompare.nj.nj_matrix(self.A, self.otus)
        expected = {0: [('E', 1.0), ('C', 0.0)], 1: [('D', 0.0), ('B', 1.0)], 2: [('A', 1.5), (0, 0.0)], 3: [(2, 0.0), (1, 0.625)]}

        self.assertEquals(sorted(res.keys()), sorted(expected.keys()))
        self._v_dict(res, expected)

    def testCreateMatrix(self):
        docs_names = ['n1', 'c2', 'd3']
        d1, d2, d3 = map(DocumentMock, docs_names)
        conn = [(d1, d2, 0.01), (d3, d1, 0.90), (d2, d3, 0.5)]
        matrix_expect = [[0, 0.99, 1 - 0.9], [0.99, 0.0, 0.5], [1 - 0.9, 0.5, 0.0]]

        matrix = codecompare.nj._create_matrix([d1, d2, d3], conn)
        self.assertEquals(matrix, matrix_expect)

        res = codecompare.nj.nj([d1, d2, d3], conn)
        expected = {0: [('c2', 0.99), ('n1', 0.0)], 1: [(0, 0.195), ('d3', 0)]}
        self._v_dict(res, expected)

    def testMerge(self):
        res = {0: [('E', 1.0), ('C', 0.0)], 1: [('D', 0.0), ('B', 1.0)], 2: [('A', 1.5), (0, 0.0)], 3: [(2, 0.0), (1, 0.625)]}
        clone = copy.deepcopy(res)
        codecompare.nj.merge(clone, 0.5)
        self.assertEquals(res, clone)
        clone = copy.deepcopy(res)
        codecompare.nj.merge(clone, 0.8)
        expected = {0: [('E', 1.0), ('C', 0.0)], 3: [('A', 1.5), (0, 0.0), ('D', 0.625), ('B', 1.625)]}
        self._v_dict(expected, clone)
        clone = copy.deepcopy(res)
        codecompare.nj.merge(clone, 1.2)
        expected = {3: [('A', 1.5), ('E', 1.0), ('C', 0.0), ('D', 0.625), ('B', 1.625)]}
        self._v_dict(expected, clone)
