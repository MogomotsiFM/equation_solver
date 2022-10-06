from equation_solver import Polynomial

class Solution:
    def __init__(self, lhs: Polynomial, rhs: Polynomial):
        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"
