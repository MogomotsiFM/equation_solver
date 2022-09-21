from linear_eq_solver import Polynomial

class ISolver:
    """
    Base class for equation solvers
    """
    def __init__(self):
        raise Exception("You may not create an instance of an abstract class")

    def solve(self, lhs: Polynomial, rhs: Polynomial):
        pass
