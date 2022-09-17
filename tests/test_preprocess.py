#from context import linear_eq_solver
from linear_eq_solver import preprocess

def test_preprocess_simple():
    # 7x - 2 = 21
    q = "7x - 2 = 21"

    lhs, rhs = preprocess(q)

    assert lhs == ['7x', '-', '2']
    assert rhs == ['21']

def test_preprocess_somewhat_complex():
    # 2(4x + 3) + 6 = 24 -4x
    q = "2( 4x + 3 ) + 6 = 24 - 4x"

    lhs, rhs = preprocess(q)

    assert lhs == ['2(', '4x', '+', '3', ')', '+', '6']
    assert rhs == ['24', '-', '4x']

def test_preprocess_simplify_both_sides():
    # 2(4x + 3) + 6 = 2(-2x + 10) + 4
    q = "2( 4x + 3 ) + 6 = 2( - 2x + 10 ) + 4"

    lhs, rhs = preprocess(q)

    assert lhs == ['2(', '4x', '+', '3', ')', '+', '6']
    assert rhs == ['2(', '-', '2x', '+', '10', ')', '+', '4']

def test_preprocess_missing_right_hand_side():
    # 2(4x + 3) + 6
    q = "2( 4x + 3 ) + 6"

    lhs, rhs = preprocess(q)

    assert lhs == ['2(', '4x', '+', '3', ')', '+', '6']
    assert rhs == ['0']

