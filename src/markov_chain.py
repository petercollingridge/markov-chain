

class Chain:
    """ A Markov chain, consisting of nodes and edges. """
    nodes = []
    edges = []


class Node:
    """ A node in a Markov chain. """

    def __init__(self, index, label=None):
        self.index = index
        self.label = label
        self.edges_in = []
        self.edges_out = []


class Edge:
    """ An edge representing the transition between two states in a Markov chain. """

    def __init__(self, node1, node2, probability):
        self.node1 = node1
        self.node2 = node2
        self.probability = probability
