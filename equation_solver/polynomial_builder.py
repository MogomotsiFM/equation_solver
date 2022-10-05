from functools import reduce

from equation_solver import Monomial
from equation_solver import Polynomial


def build_polynomial(*args):
    """
    Takes a list of Polynomial and Monomials and add them together to build a Polynomial
    """
    initial = Polynomial(Monomial(0, 0))
    poly = reduce( lambda part, term: part.add(term), args, initial )

    return poly