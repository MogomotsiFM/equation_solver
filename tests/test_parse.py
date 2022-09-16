import pytest

#from context import linear_eq_solver
from linear_eq_solver import parse

def test_parser_no_simplification_required():
    # 2x - 1
    txt = ['2x', '-', '1']

    exp = parse(txt)

    assert str(exp) == "2x - 1"

def test_parser_simplify_zeroth_order_terms():
    # 3(2x - 1) + 2
    lst = ['3(', '2x', '-', '1', ')', '+', '2']

    exp = parse(lst)

    assert str(exp) == "6x - 1"

def test_parser_simplify_first_order_terms():
    # 3(2x - 1) - 2x
    lst = ['3(', '2x', '-', '1', ')', '-', '2x']

    exp = parse(lst)

    assert str(exp) == "4x - 3"

def test_parser_simplify_expression():
    # 3(2x - 1) - 1 - 2x

    lst = ['3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp = parse(lst)

    assert str(exp) == "4x - 4"


def test_parser_frivolous_simplifications():
    # 2x - 3(2x - 1) - 1 - 2x
    lst = ['2x', '-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp = parse(lst)

    assert str(exp) == "- 6x + 2"


def test_parser_frivolous_scalar_simplification():
    # 2 + 3(2x - 1 + 5) - 1 - 2x - 3
    lst = ['2', '+', '3(', '2x', '-', '1', '+', '5', ')', '-', '1', '-', '2x', '-', '3']

    exp = parse(lst)

    assert str(exp) == "4x + 10"

def test_parser_client_error():
    with pytest.raises(Exception) as exc:
        # 3(2x - 1) - 1 - 2x + 
        lst = ['3(', '2x', '-', '1', ')', '-', '1', '-', '2x', '+']

        exp = parse(lst)
        
    assert str(exc.value) == "Ill-formatted question"

def test_parser_leading_negative_sign():
    # - 3(2x - 1) - 1 - 2x
    lst = ['-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp = parse(lst)

    assert str(exp) == "- 8x + 2"

def test_parser_leading_negative_sign0():
    # 1 - 3(2x - 1) - 1 - 2x
    lst = ['1', '-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp = parse(lst)

    assert str(exp) == "- 8x + 3"

def test_parser_implied_one_multiplier():
    # (2x - 1) + 6
    lst = ['(', '2x', '-', '1', ')', '+', '6']

    exp = parse(lst)

    assert str(exp) == '2x + 5'

def test_parser_implied_one_multiplier_():
    # 1 + (2x - 1) + 6
    lst = ['1', '+', '(', '2x', '-', '1', ')', '+', '6']

    exp = parse(lst)

    assert str(exp) == '2x + 6'

def test_parser_nested_brackets():
    # (3x - 2(x+1)) + 5x
    lst = ['(', '3x', '-', '2(', 'x', '+', '1', ')', ')', '+', '5x']

    exp = parse(lst)

    assert str(exp) == '6x - 2'

def test_parser_simple_math():
    # - 3 + 2 == 2 - 3
    lst = ['-', '3', '+', '2']
    lst2 = ['2', '-', '3']

    exp = parse(lst)
    exp2 = parse(lst2)

    assert str(exp) == str(exp2)
    assert str(exp) == "- 1"

def test_parser_multiplying_brackets():
    # (1 + 6)(x - 3)
    lst = ['(', '1', '+', '6', ')', '(', 'x', '-', '3', ')']

    exp = parse(lst)

    assert str(exp) == '7x - 21'