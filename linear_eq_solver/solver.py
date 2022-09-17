from linear_eq_solver import preprocess
from linear_eq_solver.expression import Expression

def solve(q: str):
    steps = []
    steps.append(q)

    (lhs, rhs, sub_steps) = preprocess(q)
    steps.extend(sub_steps)

    steps.append('\n{} = {}'.format(lhs, rhs))
    
    a = Expression(0, rhs.x1)
    if a.x1:
        if a.x1 > 0:
            steps.append("\nSubtract {} on both sides of the equal sign and then simplify".format(a))
        else:
            steps.append("\nAdd {} on both sides of the equal sign and then simplify".format(a.mult(-1)))
        lhs = lhs.subt( a )
        rhs = rhs.subt( a )
        steps.append('\n{} = {}'.format(lhs, rhs))


    b = Expression(lhs.x0, 0)
    if b.x0:
        if b.x0 > 0:
            steps.append("\nSubtract {} on both sides of the equal sign and then simplify".format(b))
        else:
            steps.append("\nAdd {} on both sides of the equal sign and then simplify".format(b.mult(-1)))
        rhs = rhs.subt( b )
        lhs = lhs.subt( b )
        steps.append('\n{} = {}'.format(lhs, rhs))

    if lhs.x1:
        d = 1/lhs.x1
        steps.append("\nDevide both sides by {}".format(lhs.x1))
        lhs = lhs.mult(d)
        rhs = rhs.mult(d)
        
    steps.append('\n{} = {}'.format(lhs, rhs))
    return lhs, rhs, steps
