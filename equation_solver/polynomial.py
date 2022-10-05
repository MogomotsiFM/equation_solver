import copy

from itertools import product
from functools import reduce

from decimal import Decimal

from equation_solver import Monomial

class Polynomial(Monomial):
    '''
    Uses a dictionary to represent a polynomial
    The key is the exponent and the value a Monomial

    This representation means that we are duplicating exponent data but it
    allows us to say a Polynomial has a number of Monomials
    '''
    def __init__(self, other):
        self.expression = {}
        if isinstance(other, Polynomial):
            self.expression = copy.deepcopy(other.expression)
        elif isinstance(other, Monomial):
            self.expression[other.exponent] = copy.copy(other)
        elif isinstance(other, (int, float, Decimal)):
            self.expression[0] = Monomial(other, 0)
        else:
            raise Exception("A polynomial may only be constructed from a monomial or another polynomial .")

    def add(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for term in other.expression.values():
                tmp.expression[term.exponent] = tmp.get_monomial(term.exponent).add(term)
            return tmp.simplify()
        elif isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.get_monomial(other.exponent).add(other)
            return tmp.simplify()
        raise Exception("A poly may be added to another poly or monomial.") 
            
    def subt(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for term in other.expression.values():
                tmp.expression[term.exponent] = tmp.get_monomial(term.exponent).subt(term)
            return tmp.simplify()
        elif isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.get_monomial(other.exponent).subt(other)
            return tmp.simplify()
        raise Exception("A poly may be subtracted from another poly or Monomial.")

    def mult(self, other):
        if isinstance(other, Polynomial):
            monos = [ ts[0].mult(ts[1]) for ts in product(self.expression.values(), other.expression.values()) ]
            # This is a builder and has been moved to its own file.
            # Does python support forward definitions so that we can use a type before it is defined.
            # That would allow the use of this function here before Polynomial is fully defined.
            poly = build_polynomial( *monos )
            #poly = Polynomial(0)
            #poly.expression = {item.exponent:poly.get_monomial(item.exponent).add(item) for item in monos}
            return poly.simplify()
        elif isinstance(other, (int, float, Decimal, Monomial)):
            tmp = Polynomial(self)
            for exponent, term in self.expression.items():
                tmp.expression[exponent] = term.mult(other)
            return tmp.simplify()
        raise Exception("A poly may be multiplied with a number or Monomial.")

    def div(self, other):
        if isinstance(other, Polynomial) and other.order() == 1:
            return self.long_division(other)
        elif isinstance(other, (int, float, Decimal, Monomial)):
            tmp = Polynomial(Monomial(0, 0))
            for term in self.expression.values():
                t = term.div(other)
                tmp.expression[t.exponent] = t
            return tmp.simplify()
        
        raise Exception("A poly may be divided with a number, Monomial or linear Polynomial.")

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            res = self.add( other.mult(-1) )
            
            return len(res.expression) == 1 and res.get_monomial(res.order()).coeff == 0
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

    def order(self):
        return max(self.expression.keys())

    def simplify(self):
        order = self.order()
        while(  self.get_monomial(order).coeff == 0 and len(self.expression) > 1 ):
            self.expression.pop(order)
            order = self.order()

        return self

    def long_division(self, linear):
        # Assert the linear expression is a factor
        if not self.is_factor(linear):
            raise Exception("We may only divide by a factor of a Polynomial")

        return_poly = Polynomial(0)

        divident = Polynomial(self)
        divisor = linear
        order = divident.order()
        quotient = divident.get_monomial(order).div(divisor.get_monomial(1))
        
        return_poly = return_poly.add(quotient)
        
        poly = divisor.mult(quotient)
        rem = divident.add(poly.mult(-1))

        while rem != Polynomial(0):
            divident = rem
            order = divident.order()
            quotient = divident.get_monomial(order).div(divisor.get_monomial(1))
        
            return_poly = return_poly.add(quotient)
        
            poly = divisor.mult(quotient)
            rem = divident.add(poly.mult(-1))
        
        return return_poly

    def is_factor(self, linear):
        const = linear.get_monomial(0).coeff

        return self.evaluate(-1 * const) == 0

    def evaluate(self, const):
        if (isinstance(const, (int, float, Decimal))):
            return sum([n.evaluate(const) for n in self.expression.values()])
            
        raise Exception("A polynomial may only be evaluated given a constant.")

def build_polynomial(*args):
    """
    Takes a list of Polynomial and Monomials and add them together to build a Polynomial
    """
    initial = Polynomial(Monomial(0, 0))
    poly = reduce( lambda part, term: part.add(term), args, initial )

    return poly
