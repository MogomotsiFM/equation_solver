import pytest

from equation_solver import Solution, quadratic_eq_solver
from equation_solver import Monomial as Mono
from equation_solver import Polynomial as Poly
from equation_solver.polynomial_builder import build_polynomial

def test_2nd_solver_simple():
    # x^2 - 2x + 1 = 0
    lhs = build_polynomial(Mono(1, 2), Mono(-2, 1), Mono(1, 0))
    rhs = Poly(Mono(0, 0))

    sol, _ = quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    target = [Solution(Poly(Mono(1, 1)), Poly(Mono(1, 0))), Solution(Poly(Mono(1, 1)), Poly(Mono(1, 0)))]

    print(sol)
    assert helper(sol) ^ helper(target) == set()

def test_2nd_solve_degenerate_case():
    # x^2 - 5x = 0
    rhs = build_polynomial(Mono(1, 2), Mono(-5, 1))
    lhs = Poly(Mono(0, 0))

    sol, _ = quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    target = [Solution(Poly(Mono(1, 1)), Poly(Mono(0, 0))), Solution(Poly(Mono(1, 1)), Poly(Mono(5, 0)))]

    assert helper(sol) ^ helper(target) == set()

def test_2nd_solution_normalization_require():
    # x^2 - 2x + 3 = 2x^2 - 4x
    # x^2 - 2x - 3 = 0
    # (x - 3)(x + 1)
    lhs = build_polynomial(Mono(1, 2), Mono(-2, 1), Mono(3, 0))
    rhs = build_polynomial(Mono(2, 2), Mono(-4, 1))

    sol, _ = quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    target = [Solution(Poly(Mono(1, 1)), Poly(Mono(-1, 0))), Solution(Poly(Mono(1, 1)), Poly(Mono(3, 0)))]

    assert helper(sol) ^ helper(target) == set()

def test_2nd_solution_does_not_exist():
    # x^2 + 1
    lhs = build_polynomial(Mono(1, 2), Mono(1, 0))
    rhs = Poly(Mono(0, 0))

    sol, _ = quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    assert sol == []

def test_2nd_rejects_problems_of_order_3_and_higher():
    with pytest.raises(Exception) as exc:
        # x^4 + 1 = 3(x - 2)
        lhs = build_polynomial(Mono(1, 4), Mono(1, 0))
        rhs = Poly(build_polynomial(Mono(1, 1), Mono(-2, 0)).mult(3))

        quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    assert str(exc.value) == "Trying to use a second order solver for a higher order problem"

def test_2nd_rejects_lower_order_problems():
    with pytest.raises(Exception) as exc:
        # x + 1 = 3(x - 2)
        lhs = build_polynomial(Mono(1, 1), Mono(1, 0))
        rhs = Poly(build_polynomial(Mono(1, 1), Mono(-2, 0)).mult(3))

        quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

    assert str(exc.value) == "Attempting to solve a linear equation with a second order solver"

def helper(sol_list):
    return {s.lhs.get_monomial(1).coeff*s.rhs.get_monomial(0).coeff for s in sol_list}