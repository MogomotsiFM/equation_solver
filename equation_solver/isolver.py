from equation_solver import Polynomial

class ISolver:
    """
    Base class for equation solvers
    """
    def __new__(cls, *args, **kwargs):
        if cls is ISolver:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def solve(self, lhs: Polynomial, rhs: Polynomial):
        raise NotImplementedError
