import functools

from linear_eq_solver.expression import Expression as Exp
"""Simplifies an expression by distributing and the collecting like terms"""

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
            operands.append( Exp(m*int(c), 0) )
        elif 'x' in c:
            coeff = 1
            if len(c) == 2:
                coeff = c[0]

            operands.append( Exp(0, m*int(coeff)) )
        elif c in "-+":
            if c == '-' and i == start: #The leading term is negative
                operands.append(Exp())
            ops.append(c)
        elif '(' in c:
            seenOpenningBracket = True
            
            steps.append("Distribute:")
            
            mult = 1
            if len(c) == 2:
                mult = int(c[0])

            (i, exp, sub_steps) = parse_(text, i+1, mult)
            steps.extend(sub_steps)
            
            operands.append(exp)
        elif c == ')':
            break
        else:
            steps.append("Client or normalization error. Throw an exception: {}".format(c))
            raise Exception("Ill-formatted question")
        
        i = i + 1


    # Generate step information
    # If we have seen the openning bracket then we have distributed terms
    #  and we must show that step
    if seenOpenningBracket:
        sub_steps = generate_step(operands, ops)
        steps.append(sub_steps)

    #Simplify the stack by collecting like terms
    #Each element in the stack is an expression
    operands.reverse()
    ops.reverse()
        
    a = operands.pop()

    while not (len(operands)==0 or len(ops)==0):
        b = operands.pop()
        
        o = ops.pop()
        
        if o == '+':
            a = b.add(a)
        elif o == '-':
            a = a.subt(b)
        else:
            steps.append("Something went wrong during the constrution of our stacks")
            
            raise Exception("Something went wrong during the construction of our stack")

    if len(operands)!=0 or len(ops)!=0:
        steps.append("Ill-formatted question")
        raise Exception("Ill-formatted question")

    return (i, a, steps)


def generate_step(operands: list, operators: list):
    step = ""
    # We insert a 0 Expression at the begining if an expression has a leading neg number
    # So, for printing purposes, ignore it if it was inserted
    if not operands[0] == Exp(0, 0):
        step = str(operands[0])

    for b, op in zip(operands[1:], operators):
        if op == '-':
            step = step + ' ' + str(b.mult(-1))
        else:
            step = step + " " + op + " " + str(b)
    
    return step

def parse(text):
    _, exp, steps = parse_(text, 0, 1)

    return exp, steps
