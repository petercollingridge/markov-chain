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

    def set_node_depths(self):
        if not self.is_absorbing():
            raise MarkovChainPropertyError('Chain is not absorbing')

        if not self.is_connected():
            raise MarkovChainPropertyError('Chain is disjoint')

        # Set all depths to 0 to start with
        for node in self.nodes:
            node.depth = 0

        # Map node index to the depth of that node
        visited = set()

        def is_open_node(node):
            return node not in visited

        while len(visited) < len(self.nodes):
            # Find any node which has no incoming edges from nodes not already dealt with
            for node in self.nodes:
                if is_open_node(node):
                    # Get list of edges incoming edges from nodes not yet dealt with
                    edges = [edge for edge in node.edges_in if is_open_node(edge.from_node) and not edge.is_loop]
                    # If there are no edges, then select this node
                    if len(edges) == 0:
                        selected_node = node
                        edges = [edge for edge in node.edges_in if not edge.is_loop]
                        if len(edges) == 0:
                            # Depth is 0 if there are no incoming edges
                            depth = 0
                        else:
                            # Otherwise depth is one more than the maximum incoming edge
                            depth = max(edge.from_node.depth for edge in edges) + 1
                        break
            else:
                # If we can't find a node so pick the one with the smallest index
                node_index = min(node.index for node in self.nodes if is_open_node(node))
                selected_node = self.nodes[node_index]
                if len(visited) == 0:
                    depth = 0
                else:
                    depth = max(node.depth for node in visited) + 1

            # Set depth of current node
            selected_node.depth = depth
            visited.add(selected_node)

    def _get_nodes_at_depth(self):
        # Get a list, where the item at depth[i] is a list of nodes with a depth of i
        max_depth = max(node.depth for node in self.nodes)
        depths = []
        for i in range(max_depth + 1):
            depths.append([node for node in self.nodes if node.depth == i])

        return depths

    def get_node_descendants(self):
        depths = self._get_nodes_at_depth()
        node_descendants = dict()

        for nodes in depths[::-1]:
            for node in nodes:
                # Only get children with a depth greater than node's depth
                children = [child for child in node.get_children() if child.depth > node.depth]
                descendants = set(child.index for child in children)

                for child in children:
                    child_descendants = node_descendants.get(child.index)
                    if child_descendants:
                        descendants.update(child_descendants)

                node_descendants[node.index] = descendants

        return node_descendants

    def get_node_positions(self):
        self.set_node_depths()
        descendants = self.get_node_descendants()
        depths = self._get_nodes_at_depth()

        # Map node index to a coordinate in (0, 1)
        positions = [None] * len(self.nodes)

        n_depths = len(depths)
        if n_depths == 1:
            dx = 0.5
        else:
            dx = 1 / ( - 1)

        for nodes in depths:
            for node in nodes:
                positions[node.index] = dx * node.depth


class Node:
    """A node in a Markov chain."""

    def __init__(self, index, label=None):
        self.index = index
        self.label = label
        self.edges_in = []
        self.edges_out = []
        self.depth = 0

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

    def get_children(self):
        return [edge.to_node for edge in self.edges_out if not edge.is_loop]

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
