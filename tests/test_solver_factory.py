import pytest

from equation_solver import linear_solver
from equation_solver import quadratic_eq_solver
from equation_solver import solver_factory

def test_solver_factory_non_equation():
    solver_factory(0)

def test_solver_factory_linear_equation():
    solver = solver_factory(1)

    assert isinstance(solver, linear_solver.LinearSolver)

def test_solver_factory_quadratic_solver():
    solver = solver_factory(2)

    assert isinstance(solver, quadratic_eq_solver.QuadraticEqSolver)

def test_solver_factory_solver_not_defined():
    with pytest.raises(Exception) as exc:
        solver_factory(4)

    assert str(exc.value) == "Trying to solve order 4 or more problem, good luck with that."