import parsy
import functools
from equation_solver import Monomial
from equation_solver import Polynomial

# terms: A list of lists
def map_to_monomials(terms):
    # Convert all terms to Monomials
    monomials = []
    for term in terms:
        if isinstance(term, list):
            monomials.append(map_to_monomials(term))
        elif term in '-+':
            monomials.append(term)
        else:
            monomials.append(monomial(term))
    return monomials


def reduce_expression(operands: list, operators: list):
    if not len(operands) - 1 == len(operators):
        raise Exception("Ill-formatted question")

    seq = zip(operands[1:], operators)

    # If we are adding Monomials there is a very good chance we will end up with a Polynomial
    initial = Polynomial(operands[0])
    expr = functools.reduce(reduce_one_term, seq, initial)

    return expr


def reduce_one_term(partial, operand_operator_tuple):
    operand, operator = operand_operator_tuple

    if operator == '-':
        partial = partial.subt(operand)
    elif operator == '+':
        partial = partial.add(operand)
    else:
        raise Exception("Something went wrong during the construction of our stack")

    return partial


def parse_helper(terms, top_level):
    operands = []
    operators = []
    steps = []

    first_term = True
    just_seen_operator = False
    distributed = False

    for term in terms:
        if isinstance(term, list):
            coeff = Polynomial(1)
            if not just_seen_operator and len(operands) > 0:
                coeff = operands.pop()
                if isinstance(coeff, Monomial):
                    coeff = Polynomial(coeff)

            if top_level and not distributed:
                steps.append('\nDistribute:')
                distributed = True

            expr, _ = parse_helper(term, False)
            operands.append( coeff.mult(expr) )
            just_seen_operator = False
        elif term in ['-', '+']:
            just_seen_operator = True
            operators.append(term)
            if first_term:
                operands.append( Monomial(0, 0) )
        else:
            just_seen_operator = False
            operands.append(term)

        first_term = False
    
    if distributed:
        steps.append(generate_step(operands, operators))

    expr = reduce_expression(operands, operators)

    steps.append('\nAdd like terms:')
    steps.append(str(expr))

    return expr, steps


def parse(terms):
    return parse_helper( map_to_monomials(terms), True )


def generate_step(operands: list, operators: list):
    step = ""
    # We insert a 0 Expression at the begining if an expression has a leading neg number
    # So, for printing purposes, ignore it if it was inserted
    if not operands[0] == Monomial(0, 0):
        step = str(operands[0])

    for b, op in zip(operands[1:], operators):
        if op == '-':
            step = step + ' ' + str(b.mult(-1))
        else:
            step = step + " " + op + " " + str(b)

    return step


def monomial(term):
    const_term = parsy.regex('[0-9]+')
    # ax^n
    ho_term = parsy.regex('[0-9]*x(\^[0-9]+)?')

    try:
        t = const_term.parse(term)
        return Monomial(int(t), 0)
    except parsy.ParseError:
        try:
            t = ho_term.parse(term)
            coeff = 1
            idx = t.find('x')
            if idx > 0:
                coeff = int(t[:idx])
            exp = 1
            idx = t.find('^')
            if idx > 0:
                exp = int(t[idx+1:])

            return Monomial(coeff, exp)
        except parsy.ParseError:
            raise Exception("Ill-formatted input: Ensure there is a number right after ^")
