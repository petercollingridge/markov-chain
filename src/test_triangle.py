from svg_element import SVG

n = 6

svg = SVG({ 'viewBox': '0 0 {0} {0}'.format((n + 1) * 100)})
svg.add_style('.node', {'fill': '#ccc'})
svg.add_style('.node-text', {
    'text-anchor': 'end',
    'alignment-baseline': 'central',
    'font-size': '20px'
})
svg.add_style('.node-count', {
    'alignment-baseline': 'central',
    'font-size': '12px'
})

# Add nodes
for x in range(0, n + 1):
    for y in range(0, x + 1):
        px = (n + 1 - x) * 100 - 50
        py = y * 100 + 50
        svg.add_circle(px, py, 22, {'class': 'node'})
        svg.add('text', {'class': 'node-text', 'x': px + 4, 'y': py - 2}, 'w')
        svg.add('text', {'class': 'node-count', 'x': px + 5, 'y': py - 7}, x)
        svg.add('text', {'class': 'node-count', 'x': px + 5, 'y': py + 6}, y)

svg.write('test_triangle.svg')
