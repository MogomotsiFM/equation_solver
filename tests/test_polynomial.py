import pytest

from linear_eq_solver import Polynomial
from linear_eq_solver import Monomial
from linear_eq_solver.polynomial import buildPolynomial

def test_polynomial_set_correctly():
    # "3x^2"
    m = Monomial(3, 2)
    p = Polynomial(m)

    assert str(p) == '3x^2'

def test_polynomial_addition_success():
    # "3x^2 + 5x^8"
    m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x + 7x^4"
    n = buildPolynomial(Monomial(-2, 1), Monomial(7, 4))

    s = m.add(n)

    assert str(s) == '5x^8 + 7x^4 + 3x^2 - 2x'

def test_polynomial_adding_monomial_succeeds():
    # "3x^2 + 5x^8"
    m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x^10"
    n = Monomial(-2, 10)

    s = m.add(n)

    assert str(s) == '- 2x^10 + 5x^8 + 3x^2'

def test_polynomial_addition_failure():
    with pytest.raises(Exception) as exc:
        # "3x^2 + 5x^8"
        m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

        s = m.add(5)

    assert str(exc.value) == "A poly may be added to another poly or monomial."

def test_polynomial_subtration_success():
    # "3x^2 + 5x^8"
    m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

    # "-2x + 7x^4"
    n = buildPolynomial(Monomial(-2, 1), Monomial(7, 4))

    s = m.subt(n)

    assert str(s) == '5x^8 - 7x^4 + 3x^2 + 2x'

def test_polynomial_adding_monomial_succeeds():
    # "3x^2 + 5x^8"
    m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

    # "7x^4"
    n = Monomial(7, 4)

    s = m.subt(n)

    assert str(s) == '5x^8 - 7x^4 + 3x^2'

def test_polynomial_subt_failure():
    with pytest.raises(Exception) as exc:
        # "3x^2 + 5x^8"
        m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

        s = m.subt(5)

    assert str(exc.value) == "A poly may be subtracted from another poly or monomial."

def test_polynomial_scalar_multiplication_success():
    # "3x^2 + 5x^8"
    m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

    s = m.mult(-3)

    assert str(s) == "- 15x^8 - 9x^2"

def test_polynomial_nonscalar_multiplecation_failure():
    with pytest.raises(Exception) as exc:
        # "3x^2 + 5x^8"
        m = buildPolynomial(Monomial(3, 2), Monomial(5, 8))

        # -x^3
        n = Monomial(-1, 3)

        s = m.mult(n)

    assert str(exc.value) == "A poly may be multiplied with a number only."
