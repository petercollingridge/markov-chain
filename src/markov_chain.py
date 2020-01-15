import numpy as np

class MarkovChain:
    """ A Markov chain, consisting of nodes and edges. """

    def __init__(self, params=None):
        self.nodes = []
        self.edges = []

        if params:
            if type(params) == int:
                # params is a number of nodes
                self.add_nodes(params)
            else:
                # params is a list of edges
                nodes = max(max(edge) for edge in params) + 1
                self.add_nodes(nodes)
                self.add_edges(params)

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

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)

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

    def is_absorbing(self):
        return any(len(node.edges_out) == 0 for node in self.nodes)

    def get_transition_matrix(self):
        n = len(self.nodes)
        if n == 0:
            return []
        
        matrix = np.zeros((n, n))

        for edge in self.edges:
            i = edge.from_node.index
            j = edge.to_node.index
            matrix[i, j] = edge.probability

        return matrix

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
        return "Edge from {0} to {1}, p = {2}".format(
            self.from_node.index,
            self.to_node.index,
            self.probability
        )


if __name__ == "__main__":
    chain = MarkovChain([
        (0, 1, 0.02),
        (1, 0, 0.3),
        (1, 2, 0.2),
        (2, 1, 0.4),
        (2, 0, 0.02),
        (0, 2, 0.005),
    ])

    for edge in chain.edges:
        print(edge)
    print(chain.get_transition_matrix())