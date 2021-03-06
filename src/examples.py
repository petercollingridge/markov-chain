from markov_chain import MarkovChain
from errors import MarkovChainPropertyError
from utils import write_matrix_with_fractions
from draw_svg import get_chain_svg


if __name__ == "__main__":
    chain = MarkovChain(edges=[
        (0, 1, 0.02),
        (1, 0, 0.3),
        (1, 2, 0.2),
        (2, 1, 0.4),
        (2, 0, 0.02),
        (0, 2, 0.005),
    ])

    # print(chain.get_transition_matrix())

    # try:
    #     print(chain.get_expected_steps())
    # except MarkovChainPropertyError as err:
    #     print(err) 

    chain = MarkovChain(edges=[
        (0, 1, 1 / 3),
        (1, 0, 4 / 5),
        (1, 2, 1 / 5),
        (0, 3, 2 / 3),
        (3, 0, 2 / 5),
        (3, 4, 3 / 5),
    ])

    chain = MarkovChain(
        edges=[
            (0, 1, 1 / 3),
            (1, 0, 4 / 5),
            (1, 2, 1 / 5),
            (0, 3, 2 / 3),
            (3, 0, 2 / 5),
            (3, 4, 3 / 5),
            (2, 5, 1),
            (4, 5, 1 / 3),
            (4, 4, 2 / 3),
        ]
    )

    chain = MarkovChain(
        nodes=['n = 2', 'n = 1', 'END'],
        edges=[(0, 0), (0, 1), (1, 2)]
    )

    svg = get_chain_svg(chain)
    svg.write('test.svg')

    # print(chain.get_expected_steps())
    # write_matrix_with_fractions(chain.get_expected_steps())

    # write_matrix_with_fractions(chain.get_expected_steps_before_absorption())
