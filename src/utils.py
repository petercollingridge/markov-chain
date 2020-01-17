from fractions import Fraction


def write_matrix_with_fractions(matrix):
    for row in matrix:
        print(", ".join(str(Fraction(item).limit_denominator()) for item in row))