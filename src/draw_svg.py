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
        kwargs['x'] = x
        kwargs['y'] = y
        kwargs['width'] = width
        kwargs['height'] = height

        child = SVGElement('rect', kwargs)
        self.children.append(child)

        return child

    def output(self, nesting=0):
        indent = ' ' * nesting * self.indent

        svg_string = indent + '<%s' % (self.type)

        for key, value in self.attributes.items():
            svg_string += ' {0}="{1}}"'.format(key, value)

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
