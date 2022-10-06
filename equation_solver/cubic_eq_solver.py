import itertools

from equation_solver import ISolver
from equation_solver import Monomial
from equation_solver import Polynomial as Poly
from equation_solver import build_polynomial
from equation_solver import LinearSolver
from equation_solver import QuadraticEqSolver

class CubicEqSolver(ISolver):
    def __init__(self):
        self.rhs = None
        self.lhs = None

    def solve(self, lhs: Poly, rhs: Poly):
        self.lhs = lhs
        self.rhs = rhs

        print("Cubic equation solver")
        
        steps = []

        substeps = self.normalize()
        steps.extend(substeps)

        self.assert_third_order_equation()

        steps.append("\nSolve the problem using the factor theorem and long division:")
        factor, quotient, substeps = self.find_factor()
        steps.extend(substeps)

        if factor == Poly(0):
            return [], steps

        steps.append(f'({factor})({quotient}) = 0')
        steps.append(f"Which implies: {factor} = 0    OR    {quotient} = 0")

        steps.append(f"\nSolving: {factor} = 0")
        sols1, substeps = LinearSolver().solve(factor, Poly(0))
        steps.extend(substeps)

        steps.append(f"\nSolving: {quotient} = 0")
        sols2, substeps = QuadraticEqSolver().solve(quotient, Poly(0))
        steps.extend(substeps)

        sols2.extend(sols1)

        return sols2, steps

    def normalize(self):
        steps = []

        if not self.rhs == Poly(0):
            steps.append("\nMove all terms to the left hand side:")
            self.lhs = self.lhs.subt(self.rhs)
            self.rhs = self.rhs.subt(self.rhs)
            steps.append(f"{self.lhs} = {self.rhs}")

        term = self.lhs.get_monomial(3)
        if term.coeff != 1 and term.coeff != 0:
            steps.append(f"Divide both sides by the coeffecient of {term.div(term.coeff)}")
            self.lhs = self.lhs.div(term.coeff)
            steps.append(f"{self.lhs} = {self.rhs}")

        return steps

    def assert_third_order_equation(self):
        if max(self.lhs.order(), self.rhs.order()) != 3:
            raise Exception("Attempting to use a cubic solver for a non-cubic problem.")

    def find_factor(self):
        steps = []

        # All candidate factor
        # Try this infinite sequence for factors: 0, 1, -1, 2, -2, ...
        # factors = [item for p in zip(itertools.count(0, 1), itertools.count(-1, -1)) for item in p]
        factors = [item for p in zip(range(0, 10), range(-1, -10, -1)) for item in p]

        for f in factors:
            fact = build_polynomial(Monomial(1, 1), Monomial(-1*f, 0))
            steps.append(f"Trying a factor: {fact}")

            try:
                quotient = self.lhs.div(fact)
                steps.append(f"Found a factor: {fact}")
                
                return fact, quotient, steps
            except Exception:
                print("Swallowing this exception because we still have more factors to try.")


        steps.append("Could not find a factor of the cubic polynomial.")
        
        return Poly(0), Poly(0), steps





