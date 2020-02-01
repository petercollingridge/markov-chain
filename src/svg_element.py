from collections import defaultdict


class SVGElement:
    """ Generic element with attributes and potential child elements.
        Outputs as <type attribute dict> child </type>."""

    indent = 4

    def __init__(self, type, attributes=None, child=None):
        self.type = type
        self.attributes = {}
        self.children = []

        if attributes:
            self.attributes = attributes

        if child is not None:
            self.children = [child]

    def add(self, tag, attributes=None, child=None):
        """
            Create an element with given tag type and atrributes,
            and append to self.children.
            Returns the child element.
        """

        child = SVGElement(tag, attributes, child)
        self.children.append(child)
        return child

    def add_rect(self, x=0, y=0, width=0, height=0, **kwargs):
        if not params:
            params = {}

        params['x'] = x
        params['y'] = y
        params['width'] = width
        params['height'] = height

        child = SVGElement('rect', params)
        self.children.append(child)
        return child

    def add_circle(self, cx=0, cy=0, r=0, params=None):
        if not params:
            params = {}
        params['cx'] = cx
        params['cy'] = cy
        params['r'] = r

        child = SVGElement('circle', params)
        self.children.append(child)
        return child

    def output(self, nesting=0):
        indent = ' ' * nesting * self.indent

        svg_string = indent + '<%s' % (self.type)

        for key, value in self.attributes.items():
            svg_string += ' {0}="{1}"'.format(key, value)

        if self.children is None:
            svg_string += '/>'
        else:
            svg_string += '>'

            new_line = False
            for child in self.children:
                if isinstance(child, SVGElement):
                    svg_string += '\n{0}'.format(child.output(nesting + 1))
                    new_line = True
                else:
                    svg_string += child

            if new_line:
                svg_string += '\n{0}</{1}>'.format(indent, self.type)
            else:
                svg_string += '</{0}>'.format(self.type)

        return svg_string


class SVG(SVGElement):
    """ SVG element with style element and output that includes XML document string. """

    def __init__(self, attributes=None):
        SVGElement.__init__(self, 'svg', attributes)

        self.attributes['xmlns'] = 'http://www.w3.org/2000/svg'

        style_element = SVGStyleElement()
        self.styles = style_element.children
        self.children.append(style_element)

    def add_style(self, selector, attributes):
        """
            Add style with selector to self.style.children using a dictionary in
            form { property: style }
        """

        self.styles[selector].update(attributes)

    def write_to_file(self, filename):
        """ Prints output to a given filename. Add a .svg extenstion if not given. """

        import os
        if not os.path.splitext(filename)[1] == '.svg':
            filename += '.svg'

        with open(filename, 'w') as f:
            f.write(self.output())

    def write(self, filename=None):
        """ Write output to file if given a filename, otherwise return output as a string. """

        if not filename:
            return self.output()
        else:
            self.write_to_file(filename)


class SVGStyleElement(SVGElement):
    def __init__(self):
        self.children = defaultdict(dict)

    def output(self, nesting=0):
        if not self.children:
            return ''

        style_string = '\n<style>\n'

        for element, style in self.children.items():
            style_string += '  {} {{\n'.format(element)

            for key, value in style.items():
                style_string += '    {}: {};\n'.format(key, value)
            style_string += '  }\n'

        style_string += '  </style>\n'

        return style_string
