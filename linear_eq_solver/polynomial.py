from functools import reduce

from monomial import Monomial

class Polynomial(Monomial):
    '''
    Uses a dictionary to represent a polynomial
    The key is the exponent and the value is the coeffient
    '''
    def __init__(self):
        self.expression = dict()
        pass

    def __init__(self, other):
        if isinstance(other, Polynomial):
            self.expression = other.exponent.copy()
        raise Exception("A polynomial may only be constructed from another polynomial.")

    def add(self, other):
        if isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.expression.get(other.exponent, 0) + other.coeff
            return tmp
        elif isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exp, coeff in other.expression.items():
                tmp.expression[exp] = tmp.expression.get(exp, 0) + coeff
            return tmp
        raise Exception("A poly may be added to another poly or monomial.") 
            
    def subt(self, other):
        if isinstance(other, Monomial):
            tmp = Polynomial(self)
            tmp.expression[other.exponent] = tmp.expression.get(other.exponent, 0) - other.coeff
            return tmp
        elif isinstance(other, Polynomial):
            tmp = Polynomial(self)
            for exp, coeff in other.expression.items():
                tmp.expression[exp] = tmp.expression.get(exp, 0) - coeff
            return tmp
        raise Exception("A poly may be added to another poly or monomial.")

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return ( len(other.expression) == len(other.expression) and 
                reduce(lambda p, t: p and t[1] == other.expression[t[0]], other.items(), True)
            )
        return False

    def __str__(self):
        str_ = ""
        seenNonZeroTerm = False
        for exp, coeff in self.expression.items():
            if coeff > 0:
                seenNonZeroTerm = True
                str_ = str_ + " + " + str(Monomial(coeff, exp))
            elif coeff < 0:
                seenNonZeroTerm = True
                str_ = str_ + str_(Monomial(coeff, exp))


