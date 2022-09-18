from linear_eq_solver import preprocess
from linear_eq_solver import parse

def solve(q: str):
    steps = []
    steps.append(q)

    lhs, rhs = preprocess(q)

    lhs, rhs, substeps = simplify_expressions(lhs, rhs)
    steps.extend(substeps)

    lhs, rhs, substeps = eliminate_first_order_terms(lhs, rhs)
    steps.extend(substeps)

    lhs, rhs, substeps = eliminate_zeroth_order_terms(lhs, rhs)
    steps.extend(substeps)

    first_order_coeff = lhs.get_monomial(1).coeff
    if first_order_coeff:
        d = 1/first_order_coeff
        steps.append("\nDevide both sides by {}".format(first_order_coeff))
        lhs = lhs.mult(d)
        rhs = rhs.mult(d)
        
    steps.append("\nSolution:")
    steps.append('{} = {}'.format(lhs, rhs))
    return lhs, rhs, steps

def simplify_expressions(lhs, rhs):
    steps = []

    steps.append("\nSimplify LHS:")
    lhs, lhs_sub_steps = parse(lhs)
    steps.extend(append_rhs(lhs_sub_steps, " ".join(rhs)))
    
    steps.append("\nSimplify RHS:")
    rhs, rhs_sub_steps = parse(rhs)
    steps.extend(append_lhs(rhs_sub_steps, lhs))

    return lhs, rhs, steps

def eliminate_first_order_terms(lhs, rhs):
    steps = []

    a = rhs.get_monomial(1)
    if a.coeff:
        if a.coeff > 0:
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

    return lhs, rhs, steps

def eliminate_zeroth_order_terms(lhs, rhs):
    steps = []

    b = lhs.get_monomial(0)
    if b.coeff:
        if b.coeff > 0:
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

    return lhs, rhs, steps

def append_lhs(rhs_substeps: list, lhs_expr):
    '''
    When solving equations, we focus on one side first, applying mathematical concepts 
    to that side. The other side is carried along unmodified. This fuction allows us
    to carry along the LHS.
    '''
    # Note that we do not generate equations if a step ends with a colon
    # This is because those steps highlight the maths concept used
    # This is why we need this hidden functions
    def append_lhs_to_single_step(substep: str, lhs_expr):
        if substep[-1] == ':':
            return substep
        return str(lhs_expr) + ' = ' + substep

    steps = map(lambda s: append_lhs_to_single_step(s, lhs_expr), rhs_substeps)
        
    return list(steps)

def append_rhs(lhs_substeps: list, rhs_expr):
    '''
    When solving equations, we focus on one side first, applying mathematical concepts 
    to that side. The other side is carried along unmodified. This fuction allows us
    to carry along the rhs.
    '''
    # Note that we do not generate equations if a step ends with a colon
    # This is because those steps highlight the maths concept used
    # This is why we need this hidden functions
    def append_rhs_to_single_step(substep: str, rhs_expr):
        if substep[-1] == ':':
            return substep
        return substep + ' = ' + rhs_expr

    steps = map(lambda s: append_rhs_to_single_step(s, rhs_expr), lhs_substeps)
    
    return list(steps)
