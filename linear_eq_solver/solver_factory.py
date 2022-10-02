from linear_eq_solver import linear_solver
from linear_eq_solver import quadratic_eq_solver

def solver_factory(order):
    """
    Keep a map of solvers.
    Key: order of the equation,
    Value: Solver
    """

    solvers = {
            0: linear_solver.LinearSolver(),
            1: linear_solver.LinearSolver(),
            2: quadratic_eq_solver.QuadraticEqSolver()
        }

    solver = solvers.get(order)

    if solver is None:
        raise Exception("Trying to solve order 3 or more problem, good luck with that.")

    return solver

