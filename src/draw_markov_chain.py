import drawSVG
import math


class Chain:
    nodes = []
    edges = []

    def add_node(self, x, y, label=None):
        n = len(self.nodes)
        self.nodes.append(Node(n, x, y, label))

    def add_edge(self, node_index1, node_index2, label=None):
        node1 = self.nodes[node_index1]
        node2 = self.nodes[node_index2]
        self.edges.append(Edge(node1, node2, label))


class Node:
    def __init__(self, index, x, y, label=None):
        self.index = index
        self.x = x
        self.y = y
        self.label = label


class Edge:
    def __init__(self, node1, node2, label=None):
        self.node1 = node1
        self.node2 = node2
        self.label = label

    def get_ends(self, r1, r2):
        if self.node1 != self.node2:
            angle = math.atan2(self.node2.y - self.node1.y, self.node2.x - self.node1.x)
            x1 = self.node1.x + math.cos(angle) * r1
            y1 = self.node1.y + math.sin(angle) * r1
            x2 = self.node2.x + math.cos(angle + math.pi) * r2
            y2 = self.node2.y + math.sin(angle + math.pi) * r2
            return [(x1, y1), (x2, y2)]


def add_styles(svg):
    svg.addStyle('.node', {
        'fill': '#f8f8f8',
        'stroke': '#bbb'
    })

    svg.addStyle('.node-label', {
        'text-anchor': 'middle',
        'alignment-baseline': 'central',
        'fill': '#222'
    })

    svg.addStyle('.edge', {
        'stroke': 'rgb(64, 95, 237)',
        'stroke-width': '2',
        'fill': 'none'
    })

    svg.addStyle('.numerator', {
        'text-anchor': 'middle',
        'alignment-baseline': 'baseline',
        'fill': '#222',
        'font-size': '80%'
    })

    svg.addStyle('.denominator', {
        'text-anchor': 'middle',
        'alignment-baseline': 'hanging',
        'fill': '#222',
        'font-size': '80%'
    })


def add_arrows(svg):
    def_element = svg.addChildElement('defs')
    attributes = {
        'id': "arrow",
        'viewBox': "0 0 10 10",
        'refX': "5",
        'refY': "5",
        'orient': "auto-start-reverse",
    }
    marker = def_element.addChildElement('marker', attributes)
    marker.addChildElement('path', { 'd': "M0 0L10 5L0 10z", 'fill': 'rgb(64, 95, 237)' })


def draw_chain(svg, chain, size=40):
    add_styles(svg)
    add_arrows(svg)

    for node in chain.nodes:
        attributes = { 'cx': node.x, 'cy': node.y, 'r': size, 'class': 'node' }
        svg.addChildElement('circle', attributes)
        if node.label:
            attributes = { 'x': node.x, 'y': node.y, 'class': 'node-label' }
            svg.addChildElement('text', attributes, node.label)

    for edge in chain.edges:
        if edge.node1 == edge.node2:
            cx = edge.node1.x
            cy = edge.node1.y
            gap_angle = 24 * math.pi / 180
            angle1 = math.pi * 1.5 + gap_angle
            angle2 = math.pi * 1.5 - gap_angle
            control_angle_distance = size * 2.8
            x1 = cx + math.cos(angle1) * (size + 2)
            y1 = cy + math.sin(angle1) * (size + 2)
            x2 = cx + math.cos(angle2) * (size + 4)
            y2 = cy + math.sin(angle2) * (size + 4)
            cx1 = cx + math.cos(angle1) * control_angle_distance
            cy1 = cy + math.sin(angle1) * control_angle_distance
            cx2 = cx + math.cos(angle2) * control_angle_distance
            cy2 = cy + math.sin(angle2) * control_angle_distance
            path = 'M{:.2f} {:.2f}C {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}'.format(
                x1, y1, cx1, cy1, cx2, cy2, x2, y2
            )
            svg.addChildElement('path', {
                'class': 'edge',
                'd': path,
                'marker-end': "url(#arrow)"
            })
        elif edge.node1.index > edge.node2.index:
            # Backwards arrow
            nx1 = edge.node1.x
            ny1 = edge.node1.y
            nx2 = edge.node2.x
            ny2 = edge.node2.y
            angle = math.atan2(ny2 - ny1, nx2 - nx1)
            delta_angle = (-30 if angle < 0 else 30) * math.pi / 180

            angle1 = angle + delta_angle
            angle2 = angle + math.pi - delta_angle

            x1 = nx1 + math.cos(angle1) * (size + 2)
            y1 = ny1 + math.sin(angle1) * (size + 2)
            x2 = nx2 + math.cos(angle2) * (size + 4)
            y2 = ny2 + math.sin(angle2) * (size + 4)

            control_angle_distance = size * 2
            cx1 = nx1 + math.cos(angle1) * control_angle_distance
            cy1 = ny1 + math.sin(angle1) * control_angle_distance
            cx2 = nx2 + math.cos(angle2) * control_angle_distance
            cy2 = ny2 + math.sin(angle2) * control_angle_distance
            path = 'M{:.2f} {:.2f}C {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}'.format(
                x1, y1, cx1, cy1, cx2, cy2, x2, y2
            )
            svg.addChildElement('path', {
                'class': 'edge',
                'd': path,
                'marker-end': "url(#arrow)"
            })
        else:
            ends = edge.get_ends(size + 2, size + 4)

            attributes = {
                'x1': ends[0][0],
                'y1': ends[0][1],
                'x2': ends[1][0],
                'y2': ends[1][1],
                'class': 'edge',
                'marker-end': "url(#arrow)"
            }
            svg.addChildElement('line', attributes)


def draw_fraction(svg, x, y, n1, n2):
    svg.addChildElement('text', { 'class': 'numerator', 'x': x, 'y': y - 2}, n1)
    svg.addChildElement('text', { 'class': 'denominator', 'x': x, 'y': y + 3}, n2)
    svg.addChildElement('line', { 'x1': x - 5, 'y1': y, 'x2': x + 5, 'y2': y, 'stroke': 'black'})


def draw_chains_with_pairs():
    width = 300
    height = 200

    dx = 100
    dy = 100

    svg = drawSVG.SVG({ 'width': width, 'height': height })

    chain = Chain()
    chain.add_node(50, 50, '2A')
    chain.add_node(50 + dx, 50, 'End')
    chain.add_edge(0, 1)

    chain.add_node(50, 50 + dy, '2A2B')
    chain.add_node(50 + dx, 50 + dy, '2B')
    chain.add_node(50 + dx * 2, 50 + dy, 'End')
    chain.add_edge(2, 2)
    chain.add_edge(2, 3)
    chain.add_edge(3, 4)

    draw_chain(svg, chain, 24)
    svg.outputToFile('chain_1.svg')


def draw_chains_for_4x2():
    """ Markov chain for four sets of two card types, e.g. AAAABBBB """

    r = 25
    dx = 100

    width = 2 * r + 20 + dx * 4
    height = 200
    y = 100

    svg = drawSVG.SVG({ 'width': width, 'height': height })

    chain = Chain()
    chain.add_node(r + 10, y, '4A4B')
    chain.add_edge(0, 0)
    chain.add_node(r + 10 + dx, y, '2A4B')
    chain.add_edge(0, 1)
    chain.add_edge(1, 1)
    chain.add_node(r + 10 + dx * 2, y - dx / 2, '4B')
    chain.add_node(r + 10 + dx * 2, y + dx / 2, '2A2B')
    chain.add_edge(1, 2)
    chain.add_edge(1, 3)
    chain.add_edge(3, 3)
    chain.add_node(r + 10 + dx * 3, y, '2B')
    chain.add_edge(2, 4)
    chain.add_edge(3, 4)
    chain.add_node(r + 10 + dx * 4, y, 'End')
    chain.add_edge(4, 5)

    draw_chain(svg, chain, r)
    svg.outputToFile('chain_1.svg')


def draw_chains_for_4A4B():
    r = 25
    dx = 100

    width = 2 * r + 20 + dx
    height = 120
    y = 88

    svg = drawSVG.SVG({ 'width': width, 'height': height })

    chain = Chain()
    chain.add_node(r + 10, y, '4A4B')
    chain.add_edge(0, 0)
    chain.add_node(r + 10 + dx, y, '2A4B')
    chain.add_edge(0, 1)
    draw_fraction(svg, r + 10, y - 70, 4, 7)
    draw_fraction(svg, r + 10 + dx / 2, y - 15, 3, 7)

    draw_chain(svg, chain, r)
    svg.outputToFile('4A4B_chain_1.svg')


def draw_chains_for_4A2B():
    r = 25
    dx = 100
    dy = 60

    width = 2 * r + 20 + dx * 3
    height = 200
    y = 100

    svg = drawSVG.SVG({ 'width': width, 'height': height })

    chain = Chain()
    chain.add_node(r + 10, y, '4A4B')
    chain.add_node(r + 10 + dx, y, '2A4B')
    chain.add_edge(0, 1)
    chain.add_node(r + 10 + dx * 2, y - dy, '1A4B')
    chain.add_node(r + 10 + dx * 2, y + dy, '2A3B')
    chain.add_edge(1, 2)
    chain.add_edge(1, 3)
    chain.add_edge(2, 1)
    chain.add_edge(3, 1)
    chain.add_node(r + 10 + dx * 3, y - dy, '4B')
    chain.add_node(r + 10 + dx * 3, y + dy, '2A2B')
    chain.add_edge(2, 4)
    chain.add_edge(3, 5)
    # chain.add_node(r + 10 + dx * 3, y, '2B')
    # chain.add_edge(2, 4)
    # chain.add_edge(3, 4)
    # chain.add_node(r + 10 + dx * 4, y, 'End')
    # chain.add_edge(4, 5)

    draw_chain(svg, chain, r)

    svg.addChildElement('text', {'class': 'numerator', 'x': r + 10 + dx/2, 'y': y - 7}, 'E(t) = 7/3')
    svg.addChildElement('text', {'class': 'numerator', 'x': r + 10 + dx*2.5, 'y': y - dy - 7}, 'E(t) = 2')
    svg.addChildElement('text', {'class': 'numerator', 'x': r + 10 + dx*2.5, 'y': y + dy - 7}, 'E(t) = 4')

    draw_fraction(svg, r + 10 + dx * 1.6, y * 0.8, 1, 3)
    draw_fraction(svg, r + 10 + dx * 1.6, y * 1.2, 2, 3)

    draw_fraction(svg, r + 10 + dx * 1.3, y * 0.4, 4, 5)
    draw_fraction(svg, r + 10 + dx * 1.3, y * 1.6, 2, 5)

    svg.outputToFile('4A4B_chain_1.svg')


# draw_chains_for_4x2()
# draw_chains_for_4A4B()
draw_chains_for_4A2B()