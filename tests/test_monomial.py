import pytest
from linear_eq_solver import Monomial

def test_monomial_set_correctly():
    "q = 3x"

    m = Monomial(3, 1)

    assert str(m) == '3x'

def test_monomial_zero_coeff():
    m = Monomial(0, 3)

    assert str(m) == '0'

def test_monomial_set_correctly2():
    "q = 3x^5"

    m = Monomial(3, 5)

    assert str(m) == '3x^5'

def test_monomial_valid_addition():
    "3x + 5x"
    m = Monomial(3, 1)
    n = Monomial(5, 1)

    s = m.add(n)

    assert str(s) == '8x'

def test_monomial_invalid_addition():
    "3x + 5"
    with pytest.raises(Exception) as exc:
        m = Monomial(3, 1)
        n = Monomial(5, 0)

        s = m.add(n)

    assert str(exc.value) == "Only monomials of the same order may be added."

def test_monomial_valid_subtraction():
    "3x^2 - 5x^2"
    m = Monomial( 3, 2)
    n = Monomial(-5, 2)

    s = m.add(n)

    assert str(s) == '- 2x^2'

def test_monomial_invalid_subtraction():
    "3x - 5x^2"
    with pytest.raises(Exception) as exc:
        m = Monomial(3, 1)
        n = Monomial(5, 2)

        s = m.subt(n)

    assert str(exc.value) == "Only monomials of the same order may be minused."

def test_monomial_valid_multiplication():
    "-2 * 3x^2"
    m = Monomial( 3, 2)
    
    s = m.mult(-2)

    assert str(s) == '- 6x^2'

def test_monomial_with_monomial_multiplication():
    "3x * 5x^2"
    m = Monomial(3, 1)
    n = Monomial(5, 2)

    s = m.mult(n)

    assert str(s) == '15x^3'

def test_monomial_equal_to_itself():
    m = Monomial(3, 2)

    assert m == m

def test_monomial_equality_success():
    m = Monomial(3, 2)
    n = Monomial(3, 2)

    assert m == n

def test_monomial_equality_failure():
    m = Monomial(3, 2)
    n = Monomial(3, 5)

    assert not m == n

def test_monomial_equality_agains_scalar_fails():
    m = Monomial(3, 0)

    assert not m == 3