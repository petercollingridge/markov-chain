

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

    def is_connected(self):
        if len(self.nodes) == 0:
            return True

        visited = set()
        frontier = set([self.nodes[0]])

        while len(frontier) > 0:
            node = frontier.pop()
            visited.add(node)

            for edge in node.edges_out:
                next_node = edge.to_node
                if next_node not in visited:
                    frontier.add(next_node)
            
            for edge in node.edges_in:
                next_node = edge.from_node
                if next_node not in visited:
                    frontier.add(next_node)

        return len(visited) == len(self.nodes)

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

    def __str__(self):
        return "State {0}".format(self.index)


class Edge:
    """ An edge representing the transition between two states in a Markov chain. """

    def __init__(self, from_node, to_node, probability):
        self.from_node = from_node
        self.to_node = to_node
        self.probability = probability

    def __str__(self):
        return "Edge from {0} to {1}".format(self.from_node.index, self.to_node.index)


if __name__ == "__main__":
    chain = MarkovChain()
    chain.add_node()
    chain.add_node()
    chain.add_edge(0, 1)
    print(chain)

    chain2 = MarkovChain()
    chain2.add_nodes(5)
    print(chain2)
