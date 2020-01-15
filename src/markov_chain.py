

class MarkovChain:
    """ A Markov chain, consisting of nodes and edges. """

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, label=None):
        n = len(self.nodes)
        self.nodes.append(Node(n, label))

    def add_nodes(self, n):
        for _ in range(n):
            self.add_node()

    def add_edge(self, index1, index2, probability=1):
        # TODO test index exists
        node1 = self.nodes[index1]
        node2 = self.nodes[index2]

        edge = Edge(node1, node2, probability)
        self.edges.append(edge)
        node1.edges_out.append(edge)
        node2.edges_in.append(edge)

    def __str__(self):
        return "A Markov chain with {0} nodes and {1} edges".format(
            len(self.nodes),
            len(self.edges),
        )


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
    chain.add_edge(0, 1)
    print(chain)

    chain2 = MarkovChain()
    chain2.add_nodes(5)
    print(chain2)
