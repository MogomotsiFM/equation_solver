import copy
from functools import reduce

from linear_eq_solver import Monomial

class Polynomial(Monomial):
    '''
    Uses a dictionary to represent a polynomial
    The key is the exponent and the a Monomial

    This representation means that we are duplicating exponent data but it
    allows us to say a Polynomial has a number of Monomials
    '''
    def __init__(self, other):
        self.expression = {}
        if isinstance(other, Polynomial):
            self.expression = copy.deepcopy(other.expression)
        elif isinstance(other, Monomial):
            self.expression[other.exponent] = copy.copy(other)
        else:
            raise Exception("A polynomial may only be constructed from a monomial or another polynomial .")

    def add(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exponent, term in other.expression.items():
                tmp.expression[exponent] = tmp.get_monomial(exponent).add(term)
            return tmp
        elif isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.get_monomial(other.exponent).add(other)
            return tmp
        raise Exception("A poly may be added to another poly or monomial.") 
            
    def subt(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exponent, term in other.expression.items():
                tmp.expression[exponent] = tmp.get_monomial(exponent).subt(term)
            return tmp
        elif isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.get_monomial(other.exponent).subt(other)
            return tmp
        raise Exception("A poly may be subtracted from another poly or monomial.")

    def mult(self, a):
        if type(a) is int or type(a) is float:
            tmp = Polynomial(self)
            for exponent, term in self.expression.items():
                tmp.expression[exponent] = term.mult(a)
            return tmp
        raise Exception("A poly may be multiplied with a number only.")

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return ( len(other.expression) == len(other.expression) and 
                reduce(lambda p, mono: p and mono == other.get_monomial(mono.exponent), other.expression.values(), True)
            )
        return False

    def __str__(self):
        str_ = ""

        seen_non_zero_term = False
        is_first_term = True

        # We need to ensure the terms of a Polynomial are printed a certain way 
        # if our tests are to pass. 
        # Also, it is nicer if the higher order terms are printed first
        exponents = list(self.expression.keys())
        exponents.sort(reverse=True)
        
        for e in exponents:
            term = self.get_monomial(e)
            if term.coeff > 0:
                seen_non_zero_term = True
                if is_first_term:
                    str_ = str_ + str(term)
                else:
                    str_ = str_ + " + " + str(term)

                is_first_term = False
            elif term.coeff < 0:
                seen_non_zero_term = True
                if is_first_term:
                    str_ = str_ + str(term)
                else:
                    str_ = str_ + " " + str(term)

                is_first_term = False

        if not seen_non_zero_term:
            str_ = "0"

        return str_

    def get_monomial(self, exponent):
        return self.expression.get(exponent, Monomial(0, exponent))


def build_polynomial(*args):
    poly = None
    for mono in args:
        if isinstance(mono, Monomial) or isinstance(mono, Polynomial):
            if poly == None:
                poly = Polynomial(mono)
            else:
                poly = poly.add(mono)
        else:
            raise Exception("Can only build a Polynomial from Monomials or another Polynomial")

    return poly