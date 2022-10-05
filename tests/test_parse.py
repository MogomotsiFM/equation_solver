import pytest

from equation_solver import parse
from equation_solver import Monomial
from equation_solver.polynomial_builder import build_polynomial

def test_parser_no_simplification_required():
    # 2x - 1
    txt = ['2x', '-', '1']

    exp, _ = parse(txt)

    assert str(exp) == "2x - 1"

def test_parser_simplify_zeroth_order_terms():
    # 3(2x - 1) + 2
    lst = ['3(', '2x', '-', '1', ')', '+', '2']

    exp, _ = parse(lst)

    assert str(exp) == "6x - 1"

def test_parser_simplify_first_order_terms():
    # 3(2x - 1) - 2x
    lst = ['3(', '2x', '-', '1', ')', '-', '2x']

    exp, _ = parse(lst)

    assert str(exp) == "4x - 3"

def test_parser_simplify_expression():
    # 3(2x - 1) - 1 - 2x

    lst = ['3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp, _ = parse(lst)

    assert str(exp) == "4x - 4"


def test_parser_frivolous_simplifications():
    # 2x - 3(2x - 1) - 1 - 2x
    lst = ['2x', '-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp, _ = parse(lst)

    assert str(exp) == "- 6x + 2"


def test_parser_frivolous_scalar_simplification():
    # 2 + 3(2x - 1 + 5) - 1 - 2x - 3
    lst = ['2', '+', '3(', '2x', '-', '1', '+', '5', ')', '-', '1', '-', '2x', '-', '3']

    exp, _ = parse(lst)

    assert str(exp) == "4x + 10"

def test_parser_client_error():
    with pytest.raises(Exception) as exc:
        # 3(2x - 1) - 1 - 2x + 
        lst = ['3(', '2x', '-', '1', ')', '-', '1', '-', '2x', '+']

        exp, _ = parse(lst)
        
    assert str(exc.value) == "Ill-formatted question"

def test_parser_leading_negative_sign():
    # - 3(2x - 1) - 1 - 2x
    lst = ['-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp, _ = parse(lst)

    assert str(exp) == "- 8x + 2"

def test_parser_leading_negative_sign0():
    # 1 - 3(2x - 1) - 1 - 2x
    lst = ['1', '-', '3(', '2x', '-', '1', ')', '-', '1', '-', '2x']

    exp, _ = parse(lst)

    assert str(exp) == "- 8x + 3"

def test_parser_implied_one_multiplier():
    # (2x - 1) + 6
    lst = ['(', '2x', '-', '1', ')', '+', '6']

    exp, _ = parse(lst)

    assert str(exp) == '2x + 5'

def test_parser_implied_one_multiplier_():
    # 1 + (2x - 1) + 6
    lst = ['1', '+', '(', '2x', '-', '1', ')', '+', '6']

    exp, _ = parse(lst)

    assert str(exp) == '2x + 6'

def test_parser_nested_brackets():
    # (3x - 2(x+1)) + 5x
    lst = ['(', '3x', '-', '2(', 'x', '+', '1', ')', ')', '+', '5x']

    exp, _ = parse(lst)

    assert str(exp) == '6x - 2'

def test_parser_simple_math():
    # - 3 + 2 == 2 - 3
    lst = ['-', '3', '+', '2']
    lst2 = ['2', '-', '3']

    exp, _ = parse(lst)
    exp2, _ = parse(lst2)

    assert str(exp) == str(exp2)
    assert str(exp) == "- 1"

def test_parser_multiplying_brackets():
    # (1 + 6)(x - 3)
    lst = ['(', '1', '+', '6', ')(', 'x', '-', '3', ')']

    exp, _ = parse(lst)

    assert str(exp) == '7x - 21'

def test_parser_multiple_multiplying_brackets():
    # -2(x + 1)(x - 1)(-x + 1)
    lst = ['-', '2(', 'x', '+', '1', ')(', 'x', '-', '1', ')(', '-', 'x', '+', '1', ')']

    exp, _ = parse(lst)

    assert str(exp) == '2x^3 - 2x^2 - 2x + 2'

def test_parser_multiple_digits_multipliers():
    # 30(2x - 1) - 22x
    lst = ['30(', '2x', '-', '1', ')', '-', '22x']

    exp, _ = parse(lst)

    assert str(exp) == "38x - 30"

def test_parser_missing_closing_bracket_reported():
    with pytest.raises(Exception) as exc:
        # (1 + 6)(x - 3
        lst = ['(', '1', '+', '6', ')(', 'x', '-', '3']

        parse(lst)

    assert str(exc.value) == "Could not find matching closing bracket"

def test_parser_read_higher_order_terms_correctly():
    # 13x^50 + 2
    lst = ['113x^50', '+', '2']

    exp, _ = parse(lst)

    assert str(exp) == '113x^50 + 2'
    assert exp == build_polynomial(Monomial(113, 50), Monomial(2, 0))

def test_parser_expected_but_missing_exponent_failure():
    with pytest.raises(Exception) as exc:
        # 13x^ + 2
        lst = ['113x^', '+', '2']

        parse(lst)

    assert str(exc.value) == "Ill-formatted input: Ensure there is a number right after ^"