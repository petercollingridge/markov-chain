import unittest

from src.markov_chain import MarkovChain


class TestMarkovChain(unittest.TestCase):
    def test_create_chain(self):
        chain = MarkovChain()
        self.assertEqual(len(chain.nodes), 0)
        self.assertEqual(len(chain.edges), 0)
