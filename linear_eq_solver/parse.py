from linear_eq_solver.expression import Expression as Exp
"""Simplifies an expression by distributing and the collecting like terms"""

def parse_(text, pos, m):
    ops = list() #List of operations
    s = list() #List of operands/expressions

    foundOpenningBracket = False

    i = pos
    while i<len(text):
        c = text[i]

        if c.isdigit():
            s.append( Exp(m*int(c), 0) )
        elif 'x' in c:
            coeff = 1
            if len(c) == 2:
                coeff = c[0]

            s.append( Exp(0, m*int(coeff)) )
        elif c in "-+":
            if i == 0: #The leading term is negative
                s.append(Exp())
            ops.append(c)
        elif '(' in c:
            foundOpenningBracket = True
            print("Distribute")
            mult = 1
            if len(c) == 2:
                mult = int(c[0])

            (i, exp) = parse_(text, i+1, mult)

            foundOpenningBracket = False

            s.append(exp)
        elif c == ')':
            break
        else:
            print("Client or normalization error. Throw an exception: {}".format(c))
            raise Exception("Ill-formatted question")
        
        i = i + 1

    #Simplify the stack by collecting like terms
    #Each element in the stack is an expression
    s.reverse()
    ops.reverse()
    a = s.pop()
    
    step = str(a)

    while not (len(s)==0 or len(ops)==0):
        b = s.pop()
        
        o = ops.pop()
        
        step = step + " " + str(o) + " " + str(b)

        if o == '+':
            a = b.add(a)
        elif o == '-':
            a = a.subt(b)
        else:
            print("Something went wrong during the constrution of our stacks")
            raise Exception("Something went wrong during the construction of our stack")

    if len(s)!=0 or len(ops)!=0:
        raise Exception("Ill-formatted question")

    if foundOpenningBracket:
        print(step)

    return (i, a)


def parse(text):
    _, exp = parse_(text, 0, 1)
    return exp
