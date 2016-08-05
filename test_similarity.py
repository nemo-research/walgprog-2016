import unittest

import codecompare.similarity.tag as tag
import codecompare.similarity.edit as edit
import codecompare.similarity.tfidf as tfidf
import codecompare.similarity.base as base
import codecompare.similarity.tree as tree

from codecompare.documents import _DocumentNodes

class DocumentMock:

    def __init__(self, code):
        self.nodes = _DocumentNodes(code)

    def __repr__(self):
        return str(self.nodes)


class SimilaritiesTest(unittest.TestCase):

    def __test(self, strategy, code1, code2, value):
        self.assertAlmostEqual(strategy(self.codes[code1], self.codes[code2]), value, msg="Code %i - %i" % (code1, code2), delta=0.01)

    def setUp(self):
        self.codes = []
        self.codes.append(_DocumentNodes(['A', ' B', ' C', ' A', ' C']))
        self.codes.append(_DocumentNodes(['A', ' C', ' B', ' C', ' A']))
        self.codes.append(_DocumentNodes(['A', ' B', ' C', ' C', ' C']))
        self.codes.append(_DocumentNodes(['A', ' B']))
        self.codes.append(_DocumentNodes(['A', ' D']))

    def test_clone(self):
        docs = [DocumentMock(code) for code in self.codes]
        conn = base.t_clone(docs)
        for d1, d2, v in conn:
            self.assertEqual(0, v)
        conn = base.t_clone([DocumentMock(['A', 'D']), DocumentMock(['A', 'D'])])
        self.assertEqual(len(conn), 1)
        self.assertEqual(conn[0][2], 1)

    def test_token(self):
        for code1, code2, value in [(0, 1, 5 / 5.0), (0, 2, 4 / 6.0), (0, 3, 2 / 5.0), (0, 4, 1 / 6.0)]:
            self.__test(tag._token, code1, code2, value)

    def test_tokenw(self):
        for code1, code2, value in [(0, 1, 10 / 10.0), (0, 2, 8 / 10.0), (0, 3, 4 / 7.0), (0, 4, 2 / 7.0)]:
            self.__test(tag._tokenw, code1, code2, value)

    def test_edit(self):
        for code1, code2, value in [(0, 1, 1 - 2 / 5.0), (0, 2, 1 - 1 / 5.0), (0, 3, 1 - 3 / 5.0), (0, 4, 1 - 4 / 5.0)]:
            self.__test(edit._text, code1, code2, value)

    def test_tfidf(self):
        from math import log
        docs = [DocumentMock(code) for code in self.codes]
        docs_terms, docs_len, global_terms, max_freq, avg_freq = tfidf._create_docs_data(docs)
        tf = tfidf.N_TF
        idf = tfidf.T_IDF
        docs_tfidf = tfidf._create_docs_tfidf(tf, idf, docs_terms, docs_len, global_terms, max_freq, avg_freq)
        for value in [0, 1]:
            self.assertAlmostEqual(docs_tfidf[docs[value]]['A'], 0.0, delta=0.01)
            self.assertAlmostEqual(docs_tfidf[docs[value]][' B'], abs(1 / 5.0 * log(4 / 5.0)), delta=0.01)
            self.assertAlmostEqual(docs_tfidf[docs[value]][' C'], abs(2 / 5.0 * log(3 / 5.0)), delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[2]]['A'], 0.0, delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[2]][' B'], abs(1 / 5.0 * log(4 / 5.0)), delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[2]][' C'], abs(3 / 5.0 * log(3 / 5.0)), delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[3]]['A'], 0.0, delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[3]][' B'], abs(1 / 2.0 * log(4 / 5.0)), delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[4]]['A'], 0.0, delta=0.01)
        self.assertAlmostEqual(docs_tfidf[docs[4]][' D'], abs(1 / 2.0 * log(1 / 5.0)), delta=0.01)
        self.assertAlmostEqual(tfidf._sim(docs_tfidf[docs[0]], docs_tfidf[docs[1]]), 1.0, delta=0.01)
        self.assertAlmostEqual(tfidf._sim(docs_tfidf[docs[0]], docs_tfidf[docs[2]]), 0.75, delta=0.01)
        self.assertAlmostEqual(tfidf._sim(docs_tfidf[docs[0]], docs_tfidf[docs[3]]), 0.16, delta=0.01)
        self.assertAlmostEqual(tfidf._sim(docs_tfidf[docs[0]], docs_tfidf[docs[4]]), 0.0, delta=0.01)

    def test_tree_basic(self):
        A = (tree.Node("f")
             .addkid(tree.Node("d")
                     .addkid(tree.Node("a"))
                     .addkid(tree.Node("c")
                             .addkid(tree.Node("b"))))
             .addkid(tree.Node("e")))
        B = (tree.Node("f")
             .addkid(tree.Node("c")
                     .addkid(tree.Node("d")
                             .addkid(tree.Node("a"))
                             .addkid(tree.Node("b"))))
             .addkid(tree.Node("e")))
        # Two rotations (c <-> d, then c <-> a)
        self.assertEquals(tree.distance(A, B), 2)

    def test_tree_creation(self):
        expected = (tree.Node("_ROOT_")
                    .addkid(tree.Node("A")
                            .addkid(tree.Node("B"))
                            .addkid(tree.Node("C")))
                    .addkid(tree.Node("D")))
        self.assertEquals(expected, tree._create_tree('A\n B\n C\nD'.split('\n')))

if __name__ == '__main__':
    unittest.main()
