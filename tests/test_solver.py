import pytest

#from context import LinearEqSolver
from linear_eq_solver import solver
from linear_eq_solver.expression import Expression as Exp

def test_simple_case():
    # 7x - 2 = 19
    # 7x = 21
    # x = 3
    q = '7x - 2 = 19'

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp(0, 1)
    assert rhs == Exp(3, 0)


def test_not_so_simple_case():
    # 2(4x + 3) + 6x = 15 - 4x
    # 8x + 6 + 6x = 15 - 4x
    # 18x = 9
    # x = 0.5
    q = '2( 4x + 3 ) + 6x = 15 - 4x'

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp(0, 1)
    assert rhs == Exp(0.5, 0)

def test_solution_does_not_exist():
    # 7x - 2 = 7x
    # 0x = 2
    q = '7x - 2 = 7x'

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp()
    assert rhs == Exp(2, 0)

def test_not_so_simple_case_with_multiple_digit_multipliers():
    # 21(- 4x + 3) - 6x = - 31 + 14x
    # -84x + 63 - 6x = - 41 + 14x
    # -104x = -104
    # x = 1
    q = '21( - 4x + 3 ) - 6x = - 41 + 14x'

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp(0, 1)
    assert rhs == Exp(1, 0)

def test_solver_simplifying_both_sides():
    # 2(4x + 3) + 6 = 2(-2x + 10) + 16
    q = "2( 4x + 3 ) + 6 = 2( - 2x + 10 ) + 16"

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp(0, 1)
    assert rhs == Exp(2, 0)

def test_solver_missing_right_hand_side():
    # 2(4x + 3) + 6
    q = "2( 4x + 5 ) + 6"

    lhs, rhs, _ = solver.solve(q)

    assert lhs == Exp(0, 1)
    assert rhs == Exp(-2, 0)