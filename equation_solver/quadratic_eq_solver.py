import math
import itertools

from equation_solver import IHigherOrderSolver
from equation_solver import Solution
from equation_solver import Monomial
from equation_solver import Polynomial as Poly
from equation_solver import build_polynomial

from equation_solver import LinearSolver

class QuadraticEqSolver(IHigherOrderSolver):
    def __init__(self):
        self.rhs = None
        self.lhs = None

    def solve(self, lhs: Poly, rhs: Poly):
        self.lhs = lhs
        self.rhs = rhs

        print("Quadratic equation solver")

        steps = []

        substeps = self.normalize()
        steps.extend(substeps)    

        self.assert_second_order_equation()

        if self.lhs.get_monomial(0).coeff == 0:
            sol_list, substeps = self.solve_degenerate_problem()

            steps.extend(substeps)

            return sol_list, steps
        else:
            sol_list, substeps = self.solve_general_case()
            steps.extend(substeps)

            return sol_list, steps

    def assert_second_order_equation(self):
        if self.lhs.order() > 2:
            raise Exception("Trying to use a second order solver for a higher order problem")

        if self.lhs.get_monomial(2).coeff == 0:
            raise Exception("Attempting to solve a linear equation with a second order solver")

    def generate_factors(self, coeff):
        steps = []

        M = math.ceil(math.sqrt(math.fabs(coeff)))
        # Decimal allows us to work with numbers the way humans do
        # But it does not display the way we expect: Decimal('1') vs 1
        factors = [(a, int(str(coeff/a))) for a in range(-M-1, M+1) if a != 0 and coeff % a == 0]

        steps.append( str(factors) )

        return factors, steps

    def solve_degenerate_problem(self):
        steps = []

        steps.append("\nFactor out x:")
        poly = self.lhs.div(Monomial(1, 1))
        steps.append(f"x = 0    OR   {poly} = 0")

        steps.append("\nSolve the linear problem:")
        sol_list, substeps = LinearSolver().solve(poly, Poly(0))
        steps.extend(substeps)

        # This is the solution we get from factoring out x: x = 0
        sol_list.append( Solution(Poly(Monomial(1, 1)), Poly(0)) )

        return sol_list, steps

    def solve_general_case(self):
        steps = []

        steps.append("\nGenerate factors of the coefficient of the x^2:")
        x_factors, substeps = self.generate_factors( self.lhs.get_monomial(2).coeff )
        steps.extend(substeps)

        steps.append("\nGenerate factors of the constant term:")
        c_factors, substeps = self.generate_factors( self.lhs.get_monomial(0).coeff )
        steps.extend(substeps)

        steps.append("\nTest all the permutations until we find the one that solve the problem:")
        for x, c in itertools.product(x_factors, c_factors):
            poly1 = build_polynomial(Monomial(x[0], 1), Monomial(-1*c[0], 0))
            poly2 = build_polynomial(Monomial(x[1], 1), Monomial(-1*c[1], 0))
            sol_poly = poly1.mult(poly2)

            steps.append(f"    x^2 factors = {x}, constant factors = {c}, sol = {sol_poly}")

            if sol_poly == self.lhs:
                steps.append("\nFound the permutation that solves our problem:")

                steps.append("\nFactorize:")
                steps.append(f"({poly1})({poly2}) = 0")
                steps.append(f"which implies:  {poly1} = 0    OR    {poly2} = 0")

                steps.append(f"\nSolve: {poly1} = 0")
                sol_list1, substeps = LinearSolver().solve(poly1, Poly(0))
                steps.extend(substeps)

                if not poly1 == poly2:
                    steps.append(f"\nSolve: {poly2} = 0")
                    sol_list2, substeps = LinearSolver().solve(poly2, Poly(0))
                    steps.extend(substeps)

                    sol_list1.extend(sol_list2)

                return sol_list1, steps

        # Maybe the solutions are not whole numbers
        steps.append("\nCould not find factors find that solve the problem\n")
        sols, substeps = self.completing_the_square()
        steps.extend(substeps)
        return sols, steps


    def completing_the_square(self):
        steps = []

        steps.append("\nTrying completing the square:")

        const  = self.lhs.get_monomial(0)
        if const != 0:
            steps.append("\nMove the constant to the RHS:")
            self.lhs = self.lhs.subt(const)
            self.rhs = self.rhs.subt(const)
            steps.append(f"{self.lhs} = {self.rhs}")

        x_coeff = self.lhs.get_monomial(1).coeff
        poly_lhs = build_polynomial(Monomial(1, 1), Monomial(x_coeff/2, 0))
        if x_coeff != 0:
            steps.append(f"\nSquare  half the coefficient of x and add to it both sides: ({x_coeff}/2)^2")
            sq_term = Monomial(x_coeff * x_coeff/4, 0)
            steps.append(f"{self.lhs} + ({x_coeff}/2)^2 = {self.rhs} + ({x_coeff}/2)^2")
            self.lhs = self.lhs.add(sq_term)
            self.rhs = self.rhs.add(sq_term)
            
            poly_rhs = self.rhs

            steps.append("\nFactorize the RHS:")
            steps.append(f"({poly_lhs})({poly_lhs}) = {poly_rhs}")

            steps.append("\nSimplify:")
            steps.append(f"({poly_lhs})^2 = {poly_rhs}")

        coeff = self.rhs.get_monomial(0).coeff
        if coeff > 0:
            sqrt = math.sqrt(self.rhs.get_monomial(0).coeff)
            steps.append("\nTake the square root of both sides:")
            steps.append(f"{poly_lhs} = {sqrt}    OR    {poly_lhs} = - {sqrt}")

            steps.append(f"\nSolve: {poly_lhs} = {sqrt}")
            sol_list1, substeps = LinearSolver().solve(poly_lhs, Poly(sqrt))
            steps.extend(substeps)

            steps.append(f"\nSolve: {poly_lhs} = {sqrt}")
            sol_list2, substeps = LinearSolver().solve(poly_lhs, Poly(-1*sqrt))
            steps.extend(substeps)

            sol_list1.extend(sol_list2)

            return sol_list1, steps

        steps.append(f"\nSolution does not exist: Cannot compute sqrt({coeff})")
        return [Solution(self.lhs.subt(self.rhs), Poly(0))], steps
