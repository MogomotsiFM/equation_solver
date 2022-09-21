from linear_eq_solver import ISolver

from linear_eq_solver import Polynomial

class LinearSolver(ISolver):
    def __init__(self):
        self.lhs = None
        self.rhs = None

    def solve(self, lhs: Polynomial, rhs: Polynomial):
        self.lhs = lhs
        self.rhs = rhs

        steps = []

        self.assert_linear_problem()

        substeps = self.eliminate_first_order_terms()
        steps.extend(substeps)

        substeps = self.eliminate_zeroth_order_terms()
        steps.extend(substeps)

        first_order_coeff = self.lhs.get_monomial(1).coeff
        if first_order_coeff:
            d = 1/first_order_coeff
            steps.append(f"\nDevide both sides by {first_order_coeff}:")
            self.lhs = self.lhs.mult(d)
            self.rhs = self.rhs.mult(d)

        return self.lhs, self.rhs, steps

    def assert_linear_problem(self):
        if self.lhs.order() > 1 or self.rhs.order() > 1:
            raise Exception("Trying to solve a higher order equation with a linear solver")

    def eliminate_first_order_terms(self):
        steps = []

        mono = self.rhs.get_monomial(1)
        if mono.coeff:
            if mono.coeff > 0:
                steps.append(f"\nSubtract {mono} on both sides of the equal sign:")
                steps.append(f'{self.lhs} - {mono} = - {mono} + {self.rhs}')
            else:
                a_pos = mono.mult(-1)

                steps.append(f"\nAdd {a_pos} on both sides of the equal sign:")
                steps.append(f'{self.lhs} + {a_pos} = {a_pos} {self.rhs}')

            steps.append("\nSimplify both sides:")
            self.lhs = self.lhs.subt( mono )
            self.rhs = self.rhs.subt( mono )
            steps.append(f'{self.lhs} = {self.rhs}')

        return steps

    def eliminate_zeroth_order_terms(self):
        steps = []

        mono = self.lhs.get_monomial(0)
        if mono.coeff:
            if mono.coeff > 0:
                steps.append(f"\nSubtract {mono} on both sides of the equal sign:")
                steps.append(f'{self.lhs} - {mono} = {self.rhs} - {mono}')
            else:
                b_pos = mono.mult(-1)

                steps.append(f"\nAdd {b_pos} on both sides of the equal sign:")
                steps.append(f'{self.lhs} + {b_pos} = {self.rhs} + {b_pos}')
                
            steps.append("\nSimplify both sides:")
            self.rhs = self.rhs.subt( mono )
            self.lhs = self.lhs.subt( mono )
            steps.append(f'{self.lhs} = {self.rhs}')

        return steps