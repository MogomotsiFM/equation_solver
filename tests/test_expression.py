import pytest

#from context import linear_eq_solver
from linear_eq_solver.expression import Expression as Exp

def test_expression_set_correctly():
    # -3x + 1
    x0 = 1
    x1 = -3
    exp = Exp(x0, x1)

    print("test_expression_set_correctly")
    assert (exp.x0, exp.x1) == (x0, x1)

    assert str(exp).__eq__("- 3x + 1")

def test_zero_poly():
    exp = Exp(0, 0)

    assert str(exp) == "0"

def test_add_two_expressions_success():
    # -3x + 1
    exp1 = Exp(1, -3)

    #4x - 5
    exp2 = Exp(-5, 4)

    # exp1 + exp2 = -3x + 1 + (4x - 5) = x - 4
    exp = exp1.add(exp2)

    print("test_add_two_expressions_success")
    assert (exp.x0, exp.x1) == (-4, 1)

    assert str(exp).__eq__("1x - 4")

def test_expression_addition_commutative():
    # -3x + 1
    exp1 = Exp(1, -3)

    #4x - 5
    exp2 = Exp(-5, 4)

    exp = exp1.add(exp2)

    rexp = exp2.add(exp1)

    print("test_expression_addition_commutative")
    assert (exp.x0, exp.x1) == (rexp.x0, rexp.x1)

    assert str(exp) == str(rexp)

def test_expression_addition_failure():
    with pytest.raises(Exception) as exc:
        # -3x + 1
        exp1 = Exp(1, -3)

        print("test_expression_addition_failure")
        exp = exp1.add(2)
    assert "other should be an expression" == str(exc.value)

def test_expression_subtraction_success():
    # -3x + 1
    exp1 = Exp(1, -3)

    #4x - 5
    exp2 = Exp(-5, 4)

    # exp1 - exp2 = -3x + 1 - (4x - 5) = -7x + 6
    exp = exp1.subt(exp2)

    print("test_expression_subtraction_success")
    assert (exp.x0, exp.x1) == (6, -7)

    assert str(exp) == "- 7x + 6"

def test_expression_subtraction_failure():
    with pytest.raises(Exception) as exc:
        # -3x + 1
        exp1 = Exp(1, -3)

        print("test_expression_subtraction_failure")
        exp = exp1.subt(5)
    assert "other should be an expression" == str(exc.value)

def test_expression_with_scalar_multiplication_success():
    # -3x + 1
    exp1 = Exp(1, -3)

    exp = exp1.mult(3)

    print("test_expression_with_scalar_multiplication_success")
    assert (exp.x0, exp.x1) == (3, -9)

    assert str(exp) == "- 9x + 3"

def test_expression_with_non_scalar_multiplication_failure():
    with pytest.raises(Exception) as exc:
        # -3x + 1
        exp1 = Exp(1, -3)

        # 2x - 4
        exp2 = Exp(-4, 2)

        print("test_expression_with_non_scalar_multiplication_failure")
        exp = exp1.mult(exp2)
    assert "operation expects the second operand to be an integer" == str(exc.value)

def test_equal_expressions():
    exp1 = Exp(2, -2)

    exp2 = Exp(2, -2)

    assert exp1 == exp2

def test_unequal_expression():
    exp1 = Exp(2, -2)

    exp2 = Exp(2, -1)

    assert not (exp1 == exp2)

def test_expression_equals_itself():
    exp1 = Exp(2, -2)

    assert exp1 == exp1

def test_expression_printing_first_order_term_only():
    exp1 = Exp(0, -1)

    assert str(exp1) == "- 1x"

def test_expression_printing_neg_zeroth_order_term_only():
    exp = Exp(-1, 0)

    assert str(exp) == "- 1"


