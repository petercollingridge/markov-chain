from svg_element import SVG


def get_chain_svg(chain, **kwargs):
    # Get config
    border = kwargs.get('border', 10)
    node_r = kwargs.get('node_r', 24)
    dx = kwargs.get('dx', 100)
    dy = kwargs.get('dy', 50)

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

    node_coords = [(x * width, y * height) for (x, y) in positions]

    svg = SVG({ 'viewBox': view_box })

    # Add nodes
    for (cx, cy) in node_coords:
        svg.add_circle(cx, cy, node_r, { 'class': 'node' })

    # Add edges
    

    return svg
