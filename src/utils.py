from fractions import Fraction


def write_matrix_with_fractions(matrix):
    # Get 2D list of strings showing fractions
    strings = list()
    for row in matrix:
        strings.append([str(Fraction(value).limit_denominator()) for value in row])

    # Pad with two more spaces than the longest string
    padding = max(len(value) for row in strings for value in row)

    for row in strings:
        print("  ".join("{value: <{padding}}".format(value=value, padding=padding) for value in row))