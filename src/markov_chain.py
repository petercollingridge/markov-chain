

class MarkovChain:
    """ A Markov chain, consisting of nodes and edges. """
    nodes = []
    edges = []

    def add_node(self, label=None):
        n = len(self.nodes)
        self.nodes.append(Node(n, label))

    def __str__(self):
        return "A Markov chain with {0} nodes".format(len(self.nodes))



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


if __name__ == "__main__":
    chain = MarkovChain()
    chain.add_node()
    chain.add_node()
    print(chain)