import functools
from tkinter import N

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
            mono = Monomial(int(c), 0)
            operands.append( Polynomial(mono).mult(m) )
        elif 'x' in c:
            mono = retrieve_coefficient(c)
            operands.append( Polynomial(mono).mult(m) )
        elif c in "-+":
            if c == '-' and i == start: #The leading term is negative
                operands.append(Monomial(0, 0))
            ops.append(c)
        elif ')' in c:
            if len(c) == 1:
                break
            else:
                if c == ')(':
                    # Hacky: Make sure this term is inspected again since 
                    # it contains two terms that do not exactly go together
                    # We have to modify this term because everytime we see a closing 
                    # break and return to the calling function. This means that without 
                    # modifying this term we endup terminating prematurely.
                    text[i] = '#('
                    i = i - 1

                    break
                #else:
                #    raise Exception
        elif '(' in c:
            seenOpenningBracket = True
            
            steps.append("\nDistribute:")
            
            mult = 1
            if len(c) > 1:
                if c == '#(':
                    # The popped value is actually a Polynomial.
                    mult = operands.pop()
                else:
                    mult = int(c[:-1])

            (i, exp, sub_steps) = parse_(text, i+1, mult)
            
            # Did we find a matching closing bracket
            i_hack = i + 1
            
            if i>=len(text) or (not ')' in text[i] and i_hack<len(text) and not '#' in text[i_hack]):
                raise Exception("Could not find matching closing bracket")

            steps.extend(sub_steps)
            
            operands.append(exp)
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
        steps.append("\nAdd like terms:")
    if start == 0:
        steps.append(str(simple_expr))

    return (i, simple_expr, steps)

def retrieve_coefficient(term):
    coeff = 1
    # We got here because we found x in the term
    exp   = 1
    if len(term) > 1:
        idx = term.find('x')
        if idx > 0:
            coeff = term[:idx]

        # Find the exponent: ax^b
        idx = term.find('^')
        if idx > 0:
            if (idx+1) < len(term):
                exp = term[idx+1:]
            else:
                raise Exception("Ill-formatted input: Ensure there is a number right after ^")
    return Monomial(int(coeff), int(exp))

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

def parse(text: list):
    _, exp, steps = parse_(text, 0, 1)

    return exp, steps
