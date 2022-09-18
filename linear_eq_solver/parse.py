import functools

from linear_eq_solver.expression import Expression as Exp
from linear_eq_solver.monomial import Monomial
from linear_eq_solver.polynomial import Polynomial

"""Simplifies an expression by distributing and then collecting like terms"""

def parse_(text, pos, m):
    start = pos

    ops = list() #List of operations
    operands = list() #List of operands/expressions

    steps = list()
    
    seenOpenningBracket = False

    i = pos
    while i<len(text):
        c = text[i]

        if c.isdigit():
            #operands.append( Exp(m*int(c), 0) )
            operands.append(Polynomial(Monomial(m*int(c), 0)))
        elif 'x' in c:
            coeff = 1
            if len(c) > 1:
                coeff = c[:-1]

            #operands.append( Exp(0, m*int(coeff)) )
            operands.append(Polynomial(Monomial(m*int(coeff), 1)))
        elif c in "-+":
            if c == '-' and i == start: #The leading term is negative
                #operands.append(Exp())
                operands.append(Polynomial(Monomial(0, 0)))
            ops.append(c)
        elif '(' in c:
            seenOpenningBracket = True
            
            steps.append("Distribute:")
            
            mult = 1
            if len(c) > 1:
                mult = int(c[:-1])

            (i, exp, sub_steps) = parse_(text, i+1, mult)
            steps.extend(sub_steps)
            
            operands.append(exp)
        elif c == ')':
            break
        else:
            raise Exception("Ill-formatted question")
        
        i = i + 1


    # Generate step information
    # If we have seen the openning bracket then we have distributed terms
    #  and we must show that step
    # Also, we want to print the contents of our queues if we are at the root 
    # of the recursion stack because anywhere else we do not have access to the 
    # expressions we have seen before nor the ones we have not seen.
    if seenOpenningBracket and start == 0:
        sub_steps = generate_step(operands, ops)
        steps.append(sub_steps)

    simple_expr = reduce_expression(operands, ops)

    if seenOpenningBracket and start == 0:
        steps.append("Add like terms:")
    if start == 0:
        steps.append(str(simple_expr))

    return (i, simple_expr, steps)


def generate_step(operands: list, operators: list):
    step = ""
    # We insert a 0 Expression at the begining if an expression has a leading neg number
    # So, for printing purposes, ignore it if it was inserted
    #if not operands[0] == Exp(0, 0):
    if not operands[0] == Polynomial(Monomial(0, 0)):
        step = str(operands[0])

    for b, op in zip(operands[1:], operators):
        if op == '-':
            step = step + ' ' + str(b.mult(-1))
        else:
            step = step + " " + op + " " + str(b)
    
    return step

def reduce_expression(operands: list, operators: list):
    if not len(operands) - 1 == len(operators):
        raise Exception("Ill-formatted question")

    seq = zip(operands[1:], operators)

    expr = functools.reduce(reduce_one_term, seq, operands[0])

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

def parse(text: list):
    _, exp, steps = parse_(text, 0, 1)

    return exp, steps
