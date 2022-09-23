import math
import itertools

from linear_eq_solver import ISolver

from linear_eq_solver import Monomial
from linear_eq_solver import Polynomial
from linear_eq_solver import build_polynomial

from linear_eq_solver import LinearSolver

class SecondOrderEqSolver(ISolver):
    def __init__(self):
        self.rhs = None
        self.lhs = None

    def solve(self, lhs: Polynomial, rhs: Polynomial):
        self.lhs = lhs
        self.rhs = rhs
        
        steps = []

        substeps = self.normalize_equation()
        steps.extend(substeps)    

        self.assert_second_order_equation()

        if self.lhs.get_monomial(0).coeff == 0:
            steps.append("\nFactor out x")
            t1 = self.lhs.get_monomial(2)
            t2 = self.lhs.get_monomial(1)
            poly = build_polynomial(Monomial(t1.coeff, 1), Monomial(t2.coeff, 0))
            steps.append(f"x = 0    OR   {poly} = 0")

            steps.append("\nSolve the linear problem")
            self.lhs, self.rhs, substeps = LinearSolver().solve(poly, Polynomial(Monomial(0, 0)))
            steps.append(substeps)

            steps.append("\nSolution")
            steps.append(f"x = 0   OR  {self.lhs} = {self.rhs}")

            return (self.lhs, self.rhs), (), steps
        else:
            steps.append("\nCompute factors of the coefficient of the x^2")
            x_factors, substeps = self.compute_factors( self.lhs.get_monomial(2).coeff )
            steps.extend(substeps)

            steps.append("\nCompute factors of the constant term")
            c_factors, substeps = self.compute_factors( self.lhs.get_monomial(0).coeff )
            steps.extend(substeps)

            steps.append("\nTest all the permutations until we find the one that solve the problem")
            for x, c in itertools.product(x_factors, c_factors):
                poly1 = build_polynomial(Monomial(x[0], 1), Monomial(c[0], 0))
                poly2 = build_polynomial(Monomial(x[1], 1), Monomial(c[1], 0))
                sol = poly1.mult(poly2)
                
                steps.append(f"    x factors = {x}, constant factors = {c}, sol = {sol}")

                if sol == self.lhs:
                    steps.append("\nFound the combination that solves our problem:")
                    
                    steps.append("\nFactorize")
                    steps.append(f"({poly1})({poly2}) = 0")
                    steps.append(f"which implies:  {poly1} = 0    OR    {poly2} = 0")

                    steps.append(f"\nSolve: {poly1} = 0")
                    lhs1, rhs1, substeps = LinearSolver().solve(poly1, Polynomial(Monomial(0, 0)))
                    steps.extend(substeps)

                    steps.append(f"\nSolve: {poly2} = 0")
                    lhs2, rhs2, substeps = LinearSolver().solve(poly2, Polynomial(Monomial(0, 0)))
                    steps.extend(substeps)

                    steps.append("\nSolution")
                    steps.append(f"{lhs1} = {rhs1}   OR   {lhs2} = {rhs2}")

                    return (lhs1, rhs1), (lhs2, rhs2), steps

            steps.append("\nSolution does not exist")
            return (), (), steps


    def normalize_equation(self):
        steps = []

        steps.append("\nMove all terms to the left hand side:")
        self.lhs = self.lhs.subt(self.rhs)
        self.rhs = self.rhs.subt(self.rhs)
        steps.append(f"{self.lhs} = {self.rhs}")

        return steps

    def assert_second_order_equation(self):
        if self.lhs.order() > 2:
            raise Exception("Failure: Trying to use a second order solver for a higher order problem")
        
        if self.lhs.get_monomial(2) == 0:
            raise Exception("Attempting to solve a linear equation with a second order solver")

    def compute_factors(self, coeff):
        steps = []

        M = int(math.sqrt(math.fabs(coeff))) + 1
        factors = [(a, coeff//a) for a in range(-M, M) if a != 0 and coeff % a == 0]

        steps.append(str(factors))

        return factors, steps

        