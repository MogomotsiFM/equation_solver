class Monomial:
    def __init__(self, coeff, exponent):
        if type(coeff) in (int, float) and type(exponent) is int:
            self.coeff = coeff
            self.exponent = exponent
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
        if type(other) is int or type(other) is float:
            return Monomial(other*self.coeff, self.exponent)
        elif isinstance(other, Monomial):
            return Monomial(other.coeff*self.coeff, self.exponent+other.exponent)

        raise Exception("Monomials may be multiplied by a scalar or another Monomial.")

    def __str__(self):
        str_ = "0"
        if self.coeff:
            if self.coeff > 0:
                str_ = "{}".format(self.coeff)
            else:
                str_ = "- {}".format(-1*self.coeff)
        
            if self.exponent == 1:
                str_ = str_ + "x"
            elif self.exponent > 1:
                str_ = str_ + "x^{}".format(self.exponent)

        return str_

    def __eq__(self, other):
        if isinstance(other, Monomial):
            return ( self is other or
                    (self.coeff == other.coeff and self.exponent == other.exponent)
                )
        return False
