from linear_eq_solver import Polynomial

class Solution:
    def __init__(self, lhs: Polynomial, rhs: Polynomial):
        if lhs.get_monomial(0).coeff * rhs.get_monomial(1).coeff != 0:
            raise Exception("A solution is of the form: x = const")

        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs
