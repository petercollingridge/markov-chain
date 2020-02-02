from svg_element import SVG
from math import pi, cos, sin, atan2, hypot


def get_chain_svg(chain, **kwargs):
    # Get config
    border = kwargs.get('border', 10)
    node_r = kwargs.get('node_r', 24)
    dx = kwargs.get('dx', 75)
    dy = kwargs.get('dy', 60)

    full_border = border + node_r

    # Determine dimensions and viewBox
    nodes = chain.get_node_positions()
    dimensions = nodes['dimensions']
    positions = nodes['positions']

    width = (dx + node_r * 2) * (dimensions[0] - 1)
    height = (dy + node_r * 2) * (dimensions[1] - 1)
    view_box = "-{0} -{0} {1} {2}".format(
        full_border,
        width + full_border * 2,
        height + full_border * 2)

    # Set node positions
    for i, (x, y) in enumerate(positions):
        chain.nodes[i].x = x * width
        chain.nodes[i].y = y * height

    svg = SVG({ 'viewBox': view_box })

    add_styles(svg)
    add_arrows(svg)
    add_nodes(svg, chain.nodes, node_r)
    add_edges(svg, chain.edges, node_r, dx)

    return svg


def add_styles(svg):
    svg.add_style('.node', {
        'fill': '#c8c8c8'
    })

    svg.add_style('.node-label', {
        'text-anchor': 'middle',
        'alignment-baseline': 'central',
        'fill': '#222'
    })

    svg.add_style('.edge', {
        'stroke': 'rgb(64, 95, 237)',
        'stroke-width': '2',
        'fill': 'none'
    })

    svg.add_style('.numerator', {
        'text-anchor': 'middle',
        'alignment-baseline': 'baseline',
        'fill': '#222',
        'font-node_r': '80%'
    })

    svg.add_style('.denominator', {
        'text-anchor': 'middle',
        'alignment-baseline': 'hanging',
        'fill': '#222',
        'font-node_r': '80%'
    })


def add_arrows(svg):
    marker_attributes = {
        'id': "arrow",
        'viewBox': "0 0 10 10",
        'refX': "5",
        'refY': "5",
        'orient': "auto-start-reverse",
    }
    
    svg.add('defs').\
        add('marker', marker_attributes).\
        add('path', { 'd': "M0 0L10 5L0 10z", 'fill': 'rgb(64, 95, 237)' })


def add_nodes(svg, nodes, node_r):
    for node in nodes:
        svg.add_circle(node.x, node.y, node_r, { 'class': 'node' })
        if node.label:
            svg.add('text', {
                'x': node.x,
                'y': node.y,
                'class': 'node-label'
            },
            node.label)


def add_edges(svg, edges, node_r, dx):
    gap_angle = 24 * pi / 180
    loop_size = dx * 0.85

    # Distance from node center where edges start and end
    start_r = node_r + 2
    end_r = node_r + 4

    for edge in edges:
        # Node coordinates
        nx1 = edge.from_node.x
        ny1 = edge.from_node.y
        nx2 = edge.to_node.x
        ny2 = edge.to_node.y

        if edge.from_node == edge.to_node:
            # Edge looping back to the same node
            angle1 = pi * 1.5 + gap_angle
            angle2 = pi * 1.5 - gap_angle
            x1 = nx1 + cos(angle1) * start_r
            y1 = ny1 + sin(angle1) * start_r
            x2 = nx1 + cos(angle2) * end_r
            y2 = ny1 + sin(angle2) * end_r
            cx1 = nx1 + cos(angle1) * loop_size
            cy1 = ny1 + sin(angle1) * loop_size
            cx2 = nx1 + cos(angle2) * loop_size
            cy2 = ny1 + sin(angle2) * loop_size
            path = 'M{:.2f} {:.2f}C {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}'.format(
                x1, y1, cx1, cy1, cx2, cy2, x2, y2
            )
            svg.add('path', {
                'class': 'edge',
                'd': path,
                'marker-end': "url(#arrow)"
            })
        else:
            node1 = edge.from_node
            node2 = edge.to_node
            angle = atan2(ny2 - ny1, nx2 - nx1)

            # If any edges coming out of node 2 go to node 1,
            # then we have edges going in both directions
            # so draw a curved edge
            if any(edge.to_node == node1 for edge in node2.edges_out):
                sign = 1 if node1.x < node2.x else -1
                delta_angle = sign * (-8 if cos(angle) > 0 else 8) * pi / 180
                angle1 = angle + delta_angle
                angle2 = angle - delta_angle + pi

                x1 = nx1 + cos(angle1) * start_r
                y1 = ny1 + sin(angle1) * start_r
                x2 = nx2 + cos(angle2) * end_r
                y2 = ny2 + sin(angle2) * end_r
                arc_r = hypot(nx1 - nx2, ny1 - ny2) * 0.6

                path = 'M{0:.2f} {1:.2f} A{2:.2f} {2:.2f} 0 0 1 {3:.2f} {4:.2f}'.format(
                    x1, y1, arc_r, x2, y2
                )
                svg.add('path', {
                    'class': 'edge',
                    'd': path,
                    'marker-end': "url(#arrow)"
                })
            else:
                # Straight line edge
                attributes = {
                    'x1': nx1 + cos(angle) * start_r,
                    'y1': ny1 + sin(angle) * start_r,
                    'x2': nx2 + cos(angle + pi) * end_r,
                    'y2': ny2 + sin(angle + pi) * end_r,
                    'class': 'edge',
                    'marker-end': "url(#arrow)"
                }
                svg.add('line', attributes)
