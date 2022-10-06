from equation_solver import Polynomial as Poly

from equation_solver import ISolver

class IHigherOrderSolver(ISolver):
    """
    Base class for solvers of second and higher order equations
    """
    def __new__(cls, *args, **kwargs):
        if cls is ISolver:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")

        cls.lhs = Poly(0)
        cls.rhs = Poly(0)

        return object.__new__(cls, *args, **kwargs)

    def normalize(self):
        steps = []

        if not self.rhs == Poly(0):
            steps.append("\nMove all terms to the left hand side:")
            self.lhs = self.lhs.subt(self.rhs)
            self.rhs = self.rhs.subt(self.rhs)
            steps.append(f"{self.lhs} = {self.rhs}")

        order = self.lhs.order()
        coeff = self.lhs.get_monomial(order).coeff
        if coeff != 1 and coeff != 0:
            steps.append(f"\nDevide by the coefficient of x^2: {coeff}")
            self.lhs = self.lhs.div(coeff)
            self.rhs = self.rhs.div(coeff)
            steps.append(f"{self.lhs} = {self.rhs}")

        return steps