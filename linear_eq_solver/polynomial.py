from copy import deepcopy
from functools import reduce

from linear_eq_solver.monomial import Monomial

class Polynomial(Monomial):
    '''
    Uses a dictionary to represent a polynomial
    The key is the exponent and the value is the coeffient
    '''
    def __init__(self):
        """
        Represent a polynomial as a dictionary where 
            * The key is the exponent,
            * The value is a Monomial.
        This representation means that we are duplicating exponent data but it
        allows us to say a Polynomial has a number of Monomials
        """
        #self.expression = {0, Monomial(0, 0)}
        self.expression = {0, 0}

    def __init__(self, other):
        self.expression = {}
        if isinstance(other, Polynomial):
            self.expression = other.expression.copy()
            #deepcopy(other, self)
        elif isinstance(other, Monomial):
            self.expression[other.exponent] = other.coeff
        else:
            raise Exception("A polynomial may only be constructed from another polynomial.")

    def add(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exp, coeff in other.expression.items():
                tmp.expression[exp] = tmp.expression.get(exp, 0) + coeff
            return tmp
        elif isinstance(other, Monomial) and False:
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.expression.get(other.exponent, 0) + other.coeff
            return tmp
        raise Exception("A poly may be added to another poly or monomial.") 
            
    def subt(self, other):
        if isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exp, coeff in other.expression.items():
                tmp.expression[exp] = tmp.expression.get(exp, 0) - coeff
            return tmp
        elif isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.expression.get(other.exponent, 0) - other.coeff
            return tmp
        raise Exception("A poly may be subtracted from another poly or monomial.")

    def mult(self, a):
        if type(a) is int or type(a) is float:
            tmp = Polynomial(self)
            for exp, coeff in tmp.expression.items():
                tmp.expression[exp] = a*coeff
            return tmp
        raise Exception("A polynomial may be multiplied with a number only.")

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return ( len(other.expression) == len(other.expression) and 
                reduce(lambda p, t: p and t[1] == other.expression[t[0]], other.expression.items(), True)
            )
        return False

    def __str__(self):
        str_ = ""
        seen_non_zero_term = False
        for exp, coeff in self.expression.items():
            tmp = Monomial(coeff, exp)
            if coeff > 0:
                seen_non_zero_term = True
                str_ = str_ + " + " + str(tmp)
            elif coeff < 0:
                seen_non_zero_term = True
                str_ = str_ + str(tmp)

        if not seen_non_zero_term:
            str_ = "0"

        return str_

    def getMonomial(self, exponent):
        return Monomial(self.expression.get(exponent, 0), exponent)


