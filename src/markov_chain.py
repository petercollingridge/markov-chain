import numpy as np
from collections import defaultdict

from errors import MarkovChainPropertyError


class MarkovChain:
    """A Markov chain, consisting of nodes and edges."""

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

    def __str__(self):
        return "A Markov chain with {0} nodes and {1} edges".format(
            len(self.nodes),
            len(self.edges),
        )

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
        """ Return true if all the nodes are connected to each other. """

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
        """ Return true if any nodes have no outgoing edges. """
        return any(node.is_absorbing() for node in self.nodes)

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

    def get_expected_steps(self):
        if not self.is_absorbing():
            raise MarkovChainPropertyError('Chain is not absorbing')

        if not self.is_connected():
            raise MarkovChainPropertyError('Chain is disjoint')
        
        # Get matrix of just transisition states
        transition_states = [node for node in self.nodes if not node.is_absorbing()]
        
        # Map index in the original matrix to index in the transition state matrix
        map_indices = {node.index: i for (i, node) in enumerate(transition_states)}

        t = len(transition_states)
        Q = np.zeros((t, t))

        for edge in self.edges:
            i = map_indices.get(edge.from_node.index, -1)
            j = map_indices.get(edge.to_node.index, -1)
            if i != -1 and j != -1:
                Q[i, j] = edge.probability

        N = np.linalg.inv(np.identity(t) - Q)
        return N

    def get_expected_steps_before_absorption(self):
        N = self.get_expected_steps()
        size = N.shape[0]
        return N.dot(np.ones((size, 1)))

    def get_node_depths(self):
        if not self.is_absorbing():
            raise MarkovChainPropertyError('Chain is not absorbing')

        if not self.is_connected():
            raise MarkovChainPropertyError('Chain is disjoint')

        depths = dict()

        def is_open_node(node):
            return node.index not in depths.keys()

        while len(depths) < len(self.nodes):
            # Find any node which has no incoming edges from nodes not already dealt with
            for node in self.nodes:
                if is_open_node(node):
                    edges = [edge for edge in node.edges_in if is_open_node(edge.from_node) and not edge.is_loop]
                    if len(edges) == 0:
                        current_node = node
                        edges = [edge for edge in node.edges_in if not edge.is_loop]
                        if len(edges) == 0:
                            depth = 0
                        else:
                            depth = max(depths.get(edge.from_node.index, 0) for edge in edges) + 1
                        break
            else:
                # If we don't have a node then pick the one with the smallest index
                node_index = min(node.index for node in self.nodes if is_open_node(node))
                current_node = self.nodes[node_index]
                if len(depths) == 0:
                    depth = 0
                else:
                    depth = max(depths.values()) + 1

            depths[current_node.index] = depth

        return depths


class Node:
    """A node in a Markov chain."""

    def __init__(self, index, label=None):
        self.index = index
        self.label = label
        self.edges_in = []
        self.edges_out = []

    def is_absorbing(self):
        return len(self.edges_out) == 0

    def probabilities_sum_to_one(self):
        """ Return True if all the outgoing edge probabilities sum to 1 (or sufficiently close). """
        return abs(sum(edge.probability for edge in self.edges_out) - 1) < 1e-8

    def normalise_probabilities(self):
        n = len(self.edges_out)
        if n == 0:
            return
        
        total = sum(edge.probability for edge in self.edges_out)
        if total != 0:
            for edge in self.edges_out:
                edge.probability /= total

    def __repr__(self):
        return "<Node object {0}>".format(self.index)


class Edge:
    """An edge representing the transition between two states in a Markov chain."""

    def __init__(self, from_node, to_node, probability):
        self.from_node = from_node
        self.to_node = to_node
        self.probability = probability
        self.is_loop = from_node == to_node

    def __repr__(self):
        return "Edge from {0} to {1}, p = {2}".format(
            self.from_node.index,
            self.to_node.index,
            self.probability
        )
