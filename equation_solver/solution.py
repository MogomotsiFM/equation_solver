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
    
    def __eq__(self, other):
        if isinstance(other, Solution):
            c0 = self.lhs == other.lhs and self.rhs == other.rhs
            c1 = self.lhs == other.lhs.mult(-1) and self.rhs == other.rhs.mult(-1)
            return c0 or c1
        return False
