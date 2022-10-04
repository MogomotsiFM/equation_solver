import pytest

from decimal import Decimal

from equation_solver import Polynomial
from equation_solver import Monomial
from equation_solver import build_polynomial

def test_polynomial_set_correctly():
    # "3x^2"
    m = Monomial(3, 2)
    p = Polynomial(m)

    assert str(p) == '3x^2'

def test_polynomial_constant():
    m = Polynomial(10)

    assert str(m) == '10'

def test_polynomial_addition_success():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x + 7x^4"
    n = build_polynomial(Monomial(-2, 1), Monomial(7, 4))

    s = m.add(n)

    assert str(s) == '5x^8 + 7x^4 + 3x^2 - 2x'

def test_polynomial_adding_monomial_succeeds():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x^10"
    n = Monomial(-2, 10)

    s = m.add(n)

    assert str(s) == '- 2x^10 + 5x^8 + 3x^2'

def test_polynomial_addition_failure():
    with pytest.raises(Exception) as exc:
        # "3x^2 + 5x^8"
        m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

        s = m.add(5)

    assert str(exc.value) == "A poly may be added to another poly or monomial."

def test_polynomial_subtration_success():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x + 7x^4"
    n = build_polynomial(Monomial(-2, 1), Monomial(7, 4))

    s = m.subt(n)

    assert str(s) == '5x^8 - 7x^4 + 3x^2 + 2x'

def test_polynomial_subtracting_monomial_succeeds():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "7x^4"
    n = Monomial(7, 4)

    s = m.subt(n)

    assert str(s) == '5x^8 - 7x^4 + 3x^2'

def test_polynomial_subt_failure():
    with pytest.raises(Exception) as exc:
        # "3x^2 + 5x^8"
        m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

        s = m.subt(5)

    assert str(exc.value) == "A poly may be subtracted from another poly or Monomial."

def test_polynomial_scalar_multiplication_success():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    s = m.mult(-3)

    assert str(s) == "- 15x^8 - 9x^2"

def test_polynomial_nonscalar_multiplecation_failure():
    # "- 3x^2 + 5x^8"
    m = build_polynomial(Monomial(-3, 2), Monomial(5, 8))

    # -2x^3
    n = Monomial(-2, 3)

    s = m.mult(n)

    assert str(s) == '- 10x^11 + 6x^5'

def test_polynomial_with_polynomial_multiplication_success():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x + 7x^4"
    n = build_polynomial(Monomial(-2, 1), Monomial(7, 4))

    s = m.mult(n)

    assert str(s) == '35x^12 - 10x^9 + 21x^6 - 6x^3'

def test_unequal_polynomials():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "3x^4 + 5x^8"
    n = build_polynomial(Monomial(3, 4), Monomial(5, 8))

    assert not n == m

def test_equal_polynomials():
    # "3x^2 + 5x^8"
    m = build_polynomial(Monomial(3, 2), Monomial(5, 8))

    # "5x^8 + 3x^2"
    n = build_polynomial(Monomial(5, 8), Monomial(3, 2))

    assert n == m

def test_equality_symmetric():
    # x^2 + 1 ? x^2 + 2x + 1
    m = build_polynomial(Monomial(1, 2), Monomial(1, 0))
    n = build_polynomial(Monomial(1, 2), Monomial(2, 1), Monomial(1, 0))

    assert m != n
    assert n != m

def test_polynomial_evaluate_at_constant():
    # 4x^4 - 3x^2 + 2x - 5
    m = build_polynomial(Monomial(4, 4), Monomial(-3, 2), Monomial(2, 1), Monomial(-5, 0))

    val = m.evaluate(-4)

    assert val == Decimal(963)

def test_polynomial_evaluate_at_zero():
    # 4x^4 - 3x^2 + 2x - 5
    m = build_polynomial(Monomial(4, 4), Monomial(-3, 2), Monomial(2, 1), Monomial(-5, 0))

    val = m.evaluate(0)

    assert val == Decimal(-5)

def test_polynomial_is_factor():
    # divident = x^3 - 1
    # divisor = x - 1

    divident = build_polynomial(Monomial(1, 3), Monomial(-1, 0))
    divisor = build_polynomial(Monomial(1, 1), Monomial(-1, 0))

    assert divident.is_factor(divisor) is True

def test_polynomial_is_not_factor():
    # divident = x^3 - 1
    # divisor = x + 1

    divident = build_polynomial(Monomial(1, 3), Monomial(-1, 0))
    divisor = build_polynomial(Monomial(1, 1), Monomial(1, 0))

    assert divident.is_factor(divisor) is False

def test_polynomial_long_division_by_factor():
    # divident = x^3 - 1
    # divisor = x - 1

    divident = build_polynomial(Monomial(1, 3), Monomial(-1, 0))
    divisor = build_polynomial(Monomial(1, 1), Monomial(-1, 0))

    quotient = divident.long_division(divisor)

    assert str(quotient) == 'x^2 + x + 1'

def test_polynomial_long_division_by_non_factor():
    with pytest.raises(Exception) as exc:
        # divident = x^3 - 1
        # divisor = x + 1

        divident = build_polynomial(Monomial(1, 3), Monomial(-1, 0))
        divisor = build_polynomial(Monomial(1, 1), Monomial(1, 0))

        divident.long_division(divisor)

    assert str(exc.value) == "We may only divide by a factor of a Polynomial"