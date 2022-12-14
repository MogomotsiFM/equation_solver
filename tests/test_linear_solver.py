import pytest

from equation_solver import Solution
from equation_solver import Monomial
from equation_solver import Polynomial
from equation_solver import LinearSolver
from equation_solver.polynomial_builder import build_polynomial

def test_linear_solver_simple_case():
    # 7x - 2 = 19
    # 7x = 21
    # x = 3
    q_lhs = build_polynomial(Monomial(7, 1), Monomial(-2, 0))
    q_rhs = build_polynomial(Monomial(19, 0))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial(1, 1))
    assert sol[0].rhs == Polynomial(Monomial(3, 0))

def test_linear_solver_not_so_simple_case():
    # 14x + 6 = 15 - 4x
    # x = 0.5
    q_lhs = build_polynomial(Monomial(14, 1), Monomial(6, 0))
    q_rhs = build_polynomial(Monomial(15, 0), Monomial(-4, 1))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial( 1, 1))
    assert sol[0].rhs == Polynomial(Monomial(0.5, 0))

def test_linear_solver_not_so_simple_case_negative_scalar():
    # 3x + 6 = - 15 - 4x
    # x = 0.5
    q_lhs = build_polynomial(Monomial(3, 1), Monomial(6, 0))
    q_rhs = build_polynomial(Monomial(-15, 0), Monomial(-4, 1))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial( 1, 1))
    assert sol[0].rhs == Polynomial(Monomial(-3, 0))

def test_linear_solver_not_so_simple_case_zero_scalar():
    # 3x + 15 = 15 - 4x
    # x = 0
    q_lhs = build_polynomial(Monomial(3, 1), Monomial(15, 0))
    q_rhs = build_polynomial(Monomial(15, 0), Monomial(-4, 1))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial( 1, 1))
    assert sol[0].rhs == Polynomial(Monomial(0, 0))

def test_linear_solver_not_so_simple_case_negative_x_coeff():
    # -14x + 6 = 15 - 4x
    # x = -0.9
    q_lhs = build_polynomial(Monomial(-14, 1), Monomial(6, 0))
    q_rhs = build_polynomial(Monomial(15, 0), Monomial(-4, 1))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial( 1, 1))
    assert str(sol[0].rhs) == "- 0.9"
    assert sol[0].rhs == Polynomial(Monomial(-9, 0).div(10))

def test_linear_solver_solution_does_not_exist():
    # 7x - 2 = 7x
    # 0x = 2
    q_lhs = build_polynomial(Monomial(7, 1), Monomial(-2, 0))
    q_rhs = Polynomial(Monomial(7, 1))

    sol, _ = LinearSolver().solve(q_lhs, q_rhs)

    assert sol[0].lhs == Polynomial(Monomial(0, 0))
    assert sol[0].rhs == Polynomial(Monomial(2, 0))

def test_linear_solver_try_solving_higher_order_problem_fails():
    with pytest.raises(Exception) as exc:
        # -2x^2 + x - 1 = 0
        q_lhs = build_polynomial(Monomial(-2, 2), Monomial(1, 1), Monomial(-1, 0))
        q_rhs = Monomial(0, 0)

        LinearSolver().solve(q_lhs, q_rhs)

    assert str(exc.value) == "Trying to solve a higher order equation with a linear solver"
