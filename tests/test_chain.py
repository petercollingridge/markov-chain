import unittest

from src.markov_chain import MarkovChain


class TestMarkovChain(unittest.TestCase):
    def test_create_empty_chain(self):
        chain = MarkovChain()
        self.assertEqual(len(chain.nodes), 0)
        self.assertEqual(len(chain.edges), 0)

    def test_create_chain_with_nodes(self):
        chain = MarkovChain(5)
        self.assertEqual(len(chain.nodes), 5)
        self.assertEqual(len(chain.edges), 0)

    def test_add_node(self):
        chain = MarkovChain()
        chain.add_node()
        chain.add_node()

        self.assertEqual(len(chain.nodes), 2)
        self.assertEqual(chain.nodes[0].index, 0)
        self.assertEqual(chain.nodes[1].index, 1)

    def test_add_nodes(self):
        chain = MarkovChain()
        chain.add_nodes(5)

        self.assertEqual(len(chain.nodes), 5)
        self.assertEqual(len(chain.edges), 0)

    def test_add_edge(self):
        chain = MarkovChain(3)
        chain.add_edge(0, 1)
        chain.add_edge(1, 2, 0.7)
        chain.add_edge(1, 2, 0.25)

        self.assertEqual(len(chain.nodes), 3)
        self.assertEqual(len(chain.edges), 3)
        self.assertEqual(len(chain.nodes[1].edges_out), 2)
        self.assertEqual(chain.nodes[1].edges_out[1].probability, 0.25)

    def test_add_edges(self):
        chain = MarkovChain(3)
        chain.add_edges(((0, 1), (1, 2, 0.75), (1, 0, 0.25)))

        self.assertEqual(len(chain.nodes), 3)
        self.assertEqual(len(chain.edges), 3)
        self.assertEqual(len(chain.nodes[1].edges_out), 2)
        self.assertEqual(chain.nodes[1].edges_out[1].probability, 0.25)


class TestMarkovChainConnection(unittest.TestCase):
    def test_two_circles(self):
        chain = MarkovChain()
        chain.add_nodes(7)
        chain.add_edge(0, 1)
        chain.add_edge(1, 2)
        chain.add_edge(2, 3)
        chain.add_edge(3, 0)
        
        chain.add_edge(4, 5)
        chain.add_edge(5, 6)
        chain.add_edge(6, 4)
        self.assertEqual(chain.is_connected(), False)

    def test_two_connected_circles(self):
        chain = MarkovChain()
        chain.add_nodes(7)
        chain.add_edge(0, 1)
        chain.add_edge(1, 2)
        chain.add_edge(2, 3)
        chain.add_edge(3, 0)
        
        chain.add_edge(4, 5)
        chain.add_edge(5, 6)
        chain.add_edge(6, 4)
        chain.add_edge(4, 0)
        self.assertEqual(chain.is_connected(), True)

    def test_all_nodes_out(self):
        chain = MarkovChain()
        chain.add_nodes(4)
        chain.add_edge(0, 1)
        chain.add_edge(0, 2)
        chain.add_edge(0, 3)

        self.assertEqual(chain.is_connected(), True)

    def test_all_nodes_in(self):
        chain = MarkovChain()
        chain.add_nodes(4)
        chain.add_edge(1, 0)
        chain.add_edge(2, 0)
        chain.add_edge(3, 0)

        self.assertEqual(chain.is_connected(), True)

