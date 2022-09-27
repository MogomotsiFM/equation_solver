"""
Momomial is an term of the form: ax^n
    The abstraction store the coefficient `a` and the exponent `n`
    along with a set of allowed operations. 
"""

import math
from decimal import Decimal

class Monomial:
    def __init__(self, coeff, exponent):
        if type(coeff) in (int, float, Decimal) and isinstance(exponent, int) and exponent >= 0:
            self.coeff = Decimal(coeff)
            self.exponent = exponent
        elif exponent < 0:
            raise Exception("All exponents should be non-negative")
        else:
            raise Exception("Both coeff and exp should be integers.")

    def add(self, other):
        if isinstance(other, Monomial) and self.exponent == other.exponent:
            return Monomial(other.coeff + self.coeff, self.exponent)
        raise Exception("Only monomials of the same order may be added.")

    def subt(self, other):
        if isinstance(other, Monomial) and self.exponent == other.exponent:
            return Monomial(self.coeff - other.coeff, self.exponent)
        raise Exception("Only monomials of the same order may be minused.")

    def mult(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Monomial(other*self.coeff, self.exponent)
        elif isinstance(other, Monomial):
            return Monomial(other.coeff*self.coeff, self.exponent+other.exponent)

        raise Exception("Monomials may be multiplied by a scalar or another Monomial.")

    def div(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Monomial(self.coeff/other, self.exponent)
        elif isinstance(other, Monomial):
            return Monomial(self.coeff/other.coeff, self.exponent-other.exponent)

        raise Exception("Monomials may be divided by a scalar or another Monomial.")

    def __str__(self):
        str_ = "0"
        if self.coeff:
            if self.coeff > 0:
                if self.coeff == 1 and self.exponent != 0:
                    str_ = ""
                else:
                    str_ = f"{self.coeff}"
            else:
                if self.coeff == -1  and self.exponent != 0:
                    str_ = '- '
                else:
                    str_ = f"- {-1*self.coeff}"
        
            if self.exponent == 1:
                str_ = str_ + "x"
            elif self.exponent > 1:
                str_ = str_ + f"x^{self.exponent}"

        return str_

    def __eq__(self, other):
        if isinstance(other, Monomial):
            return ( self is other or
                    (self.coeff == other.coeff and self.exponent == other.exponent)
                )
        return False
