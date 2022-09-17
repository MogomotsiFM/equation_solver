from linear_eq_solver import preprocess
from linear_eq_solver.expression import Expression

def solve(q: str):
    steps = []
    steps.append(q)

    (lhs, rhs, sub_steps) = preprocess(q)
    steps.extend(sub_steps)

    a = Expression(0, rhs.x1)
    if a.x1:
        if a.x1 > 0:
            steps.append("\nSubtract {} on both sides of the equal sign:".format(a))
            steps.append('{} - {} = - {} + {}'.format(lhs, a, a, rhs))
        else:
            a_pos = a.mult(-1)

            steps.append("\nAdd {} on both sides of the equal sign:".format(a_pos))
            steps.append('{} + {} = {} {}'.format(lhs, a_pos, a_pos, rhs))

        steps.append("\nSimplify both sides:")
        lhs = lhs.subt( a )
        rhs = rhs.subt( a )
        steps.append('{} = {}'.format(lhs, rhs))


    b = Expression(lhs.x0, 0)
    if b.x0:
        if b.x0 > 0:
            steps.append("\nSubtract {} on both sides of the equal sign:".format(b))
            steps.append('{} - {} = {} - {}'.format(lhs, b, rhs, b))
        else:
            b_pos = b.mult(-1)

            steps.append("\nAdd {} on both sides of the equal sign:".format(b_pos))
            steps.append('{} + {} = {} + {}'.format(lhs, b_pos, rhs, b_pos))
            
        steps.append("\nSimplify both sides:")
        rhs = rhs.subt( b )
        lhs = lhs.subt( b )
        steps.append('{} = {}'.format(lhs, rhs))

    if lhs.x1:
        d = 1/lhs.x1
        steps.append("\nDevide both sides by {}".format(lhs.x1))
        lhs = lhs.mult(d)
        rhs = rhs.mult(d)
        
    steps.append("\nSolution:")
    steps.append('{} = {}'.format(lhs, rhs))
    return lhs, rhs, steps
