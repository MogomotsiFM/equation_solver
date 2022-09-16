class Expression:
    """
    Represent each expression as a first order polynomial

    An alternative is to use the composite design pattern
    """
    def __init__(self, x0=0, x1=0):
        self.x0 = x0
        self.x1 = x1

    def add(self, other):
        if isinstance(other, Expression):
            return Expression(self.x0 + other.x0, self.x1 + other.x1)
        raise Exception("other should be an expression")

    def subt(self, other):
        if isinstance(other, Expression):
            return Expression(self.x0 - other.x0, self.x1 - other.x1)
        raise Exception("other should be an expression")

    def mult(self, a):
        if type(a) is float or type(a) is int:
            return Expression(a*self.x0, a*self.x1)
        raise Exception("operation expects the second operand to be an integer")

    def __eq__(self, other):
        return (self is other or
               (self.x0 == other.x0 and self.x1 == other.x1))

    def __str__(self):
        str_ = ""
        ho = False #Higher order term has not found
        if self.x1 > 0:
            str_ = "{}x".format(self.x1)
            ho = True
        elif self.x1 < 0:
            str_ = "- {}x".format(-1*self.x1)
            ho = True

        if self.x0 > 0:
            if ho:
                str_ = str_ + " + {}"
            else:
                str_ = "{}"
            str_ = str_.format(self.x0)
        elif self.x0 < 0:
            if ho:
                str_ = str_ + " - {}"
            else: 
                str_ = "- {}"
            str_ = str_.format(-1*self.x0)
        else:
            if not ho:
                str_ = "{}".format(self.x0)
        return str_
    

    
