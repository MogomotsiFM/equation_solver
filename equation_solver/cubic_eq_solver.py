import itertools
import math

from equation_solver import IHigherOrderSolver
from equation_solver import Monomial
from equation_solver import Polynomial as Poly
from equation_solver import build_polynomial
from equation_solver import LinearSolver
from equation_solver import QuadraticEqSolver
from equation_solver import Solution

class CubicEqSolver(IHigherOrderSolver):
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
        factor, substeps = self.find_factor()
        steps.extend(substeps)

        if factor == Poly(0):
            return [], steps

        quotient = self.lhs.div(factor)
        steps.append(f"\nLong division: ({self.lhs}) / ({factor}) = {quotient}")
        steps.append(f"Which means that: {self.lhs} = ({factor})({quotient})")
        steps.append(f'Therefore: ({factor})({quotient}) = 0')
        steps.append(f"Which means: {factor} = 0    OR    {quotient} = 0")

        steps.append(f"\nSolving: {factor} = 0")
        sols1, substeps = LinearSolver().solve(factor, Poly(0))
        steps.extend(substeps)

        steps.append(f"\nSolving: {quotient} = 0")
        sols2, substeps = QuadraticEqSolver().solve(quotient, Poly(0))
        steps.extend(substeps)
        
        # Solution does not exist
        if len(sols2) == 0:
            sols2.append(Solution(quotient, Poly(0)))

        sols2.extend(sols1)

        return sols2, steps

    def assert_third_order_equation(self):
        if max(self.lhs.order(), self.rhs.order()) != 3:
            raise Exception("Attempting to use a cubic solver for a non-cubic problem.")

    def factor(self):
        '''
        All candidate factor
        Try this infinite sequence for factors: 0, 1, -1, 2, -2, ...
        '''
        for pair in zip(itertools.count(0, 1), itertools.count(-1, -1)):
            for item in pair:
                yield item
    
    def find_factor(self):
        steps = []

        for f in itertools.takewhile(lambda f: math.fabs(f) < 50, self.factor()):
            fact = build_polynomial(Monomial(1, 1), Monomial(-1*f, 0))
            steps.append(f"Trying a factor: {fact}")

            if self.lhs.evaluate(f) == 0:
                return fact, steps

        steps.append("Could not find a factor of the cubic polynomial.")
        return Poly(0), steps





