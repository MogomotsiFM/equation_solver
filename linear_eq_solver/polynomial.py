import copy
from functools import reduce
from itertools import product

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
        raise Exception("A poly may be subtracted from another poly or Monomial.")

    def mult(self, other):
        if isinstance(other, Polynomial):
            monos = [ ts[0].mult(ts[1]) for ts in product(self.expression.values(), other.expression.values()) ]
            poly = build_polynomial( *monos )
            return poly
        elif type(other) is int or type(other) is float or isinstance(other, Monomial):
            tmp = Polynomial(self)
            for exponent, term in self.expression.items():
                tmp.expression[exponent] = term.mult(other)
            return tmp
        raise Exception("A poly may be multiplied with a number or Monomial.")

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
    initial = Polynomial(Monomial(0, 0))
    poly = reduce( lambda part, term: part.add(term), args, initial )

    return poly