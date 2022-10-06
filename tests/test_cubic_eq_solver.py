import pytest

from equation_solver import Monomial as Mono
from equation_solver import Polynomial
from equation_solver import cubic_eq_solver
from equation_solver import build_polynomial
from equation_solver import Solution

# Solution does not exist
def test_cubic_solver_solution_does_not_exist():
    # x^3 + 2x^2 + x - 3 = 0
    lhs = build_polynomial(Mono(1, 3), Mono(2, 2), Mono(1, 1), Mono(-3, 0))
    rhs = Polynomial(0)

    sol, _ = cubic_eq_solver.CubicEqSolver().solve(lhs, rhs)

    assert len(sol) == 1
    assert sol[0].lhs == lhs

# Only one solution exists, the resultant quadratic problem cannot be solved
def test_cubic_solver_one_solution_exists():
    # x^3 - 1 = (x - 1)(x^2 + x + 1)
    lhs = build_polynomial(Mono(1, 3), Mono(-1, 0))
    rhs = Polynomial(0)

    sol, _ = cubic_eq_solver.CubicEqSolver().solve(lhs, rhs)

    assert len(sol) == 2
    assert sol[0].lhs == build_polynomial(Mono(1, 2), Mono(1, 1), Mono(1, 0))
    assert sol[1] == Solution(build_polynomial(Mono(1, 1)), Polynomial(1))
    
 
# All three solutions exist
def test_cubic_solver_three_solutions_exist():
    # x^3 + x^2 - 4x - 4
    lhs = build_polynomial(Mono(1, 3), Mono(1, 2), Mono(-4, 1), Mono(-4, 0))
    rhs = Polynomial(0)

    sols, _ = cubic_eq_solver.CubicEqSolver().solve(lhs, rhs)

    x = Polynomial(Mono(1, 1))
    target = [Solution(x, Polynomial(-1)), 
              Solution(x, Polynomial(-2)), 
              Solution(x, Polynomial(2))]
    assert all( [s in sols for s in target] )

# Trying to solve a problem of order greater than three fails
def test_cubic_solver_fifth_order_equation_fails():
    with pytest.raises(Exception) as exc:
        # x^5 - 1
        lhs = build_polynomial(Mono(1, 5), Mono(-1, 0))
        rhs = Polynomial(0)

        cubic_eq_solver.CubicEqSolver().solve(lhs, rhs)

    assert str(exc.value) == "Attempting to use a cubic solver for a non-cubic problem."

# Attempting to solve a problem of order lower than three fails
def test_cubic_solver_second_order_equation_fails():
    with pytest.raises(Exception) as exc:
        # x^2 - 1
        lhs = build_polynomial(Mono(1, 2), Mono(-1, 0))
        rhs = Polynomial(0)

        cubic_eq_solver.CubicEqSolver().solve(lhs, rhs)

    assert str(exc.value) == "Attempting to use a cubic solver for a non-cubic problem."