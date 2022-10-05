from equation_solver import ISolver
from equation_solver import LinearSolver
from equation_solver import QuadraticEqSolver
from equation_solver import CubicEqSolver

def solver_factory(order) -> ISolver:
    """
    Keep a map of solvers.
    Key: order of the equation,
    Value: Solver
    """

    solvers = {
            0: LinearSolver(),
            1: LinearSolver(),
            2: QuadraticEqSolver(),
            3: CubicEqSolver()
        }

    solver = solvers.get(order)

    if solver is None:
        raise Exception("Trying to solve order 4 or more problem, good luck with that.")

    return solver

