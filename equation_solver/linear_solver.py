import math

from equation_solver import ISolver

from equation_solver import Polynomial
from equation_solver import Solution

class LinearSolver(ISolver):
    """
    Solver for equations of the form: ax + b = mx + c
    """
    def __init__(self):
        self.lhs = None
        self.rhs = None

    def solve(self, lhs: Polynomial, rhs: Polynomial):
        self.lhs = lhs
        self.rhs = rhs

        print("Linear equation solver")

        steps = []

        self.assert_linear_problem()

        substeps = self.eliminate_first_order_terms()
        steps.extend(substeps)

        substeps = self.eliminate_zeroth_order_terms()
        steps.extend(substeps)

        first_order_coeff = self.lhs.get_monomial(1).coeff
        if first_order_coeff != 1 and first_order_coeff != 0:
            steps.append(f"\nDevide both sides by {first_order_coeff}:")
            self.lhs = self.lhs.div(first_order_coeff)
            self.rhs = self.rhs.div(first_order_coeff)

            steps.append(f"{self.lhs} = {self.rhs}")

        sol = []
        sol.append(Solution(self.lhs, self.rhs))

        return sol, steps

    def assert_linear_problem(self):
        if self.lhs.order() > 1 or self.rhs.order() > 1:
            raise Exception("Trying to solve a higher order equation with a linear solver")

    def eliminate_first_order_terms(self):
        # steps = []

        mono = self.rhs.get_monomial(1)

        return self.collect_like_terms(mono)

    def eliminate_zeroth_order_terms(self):
        # steps = []

        mono = self.lhs.get_monomial(0)

        return self.collect_like_terms(mono)
        

    def collect_like_terms(self, term):
        steps = []

        if term.coeff:
            if term.coeff > 0:
                steps.append(f"\nSubtract {term} on both sides of the equal sign:")
                steps.append(f'{self.lhs} - {term} = {self.rhs} - {term}')
            else:
                b_pos = term.mult(-1)

                steps.append(f"\nAdd {b_pos} on both sides of the equal sign:")
                steps.append(f'{self.lhs} + {b_pos} = {self.rhs} + {b_pos}')
                
            steps.append("\nSimplify both sides:")
            self.rhs = self.rhs.subt( term )
            self.lhs = self.lhs.subt( term )
            steps.append(f'{self.lhs} = {self.rhs}')

        return steps