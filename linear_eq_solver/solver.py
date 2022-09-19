"""
Solves linear equations
"""

from linear_eq_solver import preprocess
from linear_eq_solver import parse

def solve(q: str):
    """
    Takes a linear equation
    Returns the solution as a lhs and rhs pair
        The third return value is a list of maths step taken in solving the problem
    """
    steps = []
    steps.append(q)

    lhs, rhs = preprocess(q)

    lhs, rhs, substeps = simplify_expressions(lhs, rhs)
    steps.extend(substeps)

    assert_linear_problem(lhs)
    assert_linear_problem(rhs)

    lhs, rhs, substeps = eliminate_first_order_terms(lhs, rhs)
    steps.extend(substeps)

    lhs, rhs, substeps = eliminate_zeroth_order_terms(lhs, rhs)
    steps.extend(substeps)

    first_order_coeff = lhs.get_monomial(1).coeff
    if first_order_coeff:
        d = 1/first_order_coeff
        steps.append(f"\nDevide both sides by {first_order_coeff}:")
        lhs = lhs.mult(d)
        rhs = rhs.mult(d)
        
    steps.append("\nSolution:")
    steps.append(f'{lhs} = {rhs}')
    return lhs, rhs, steps

def assert_linear_problem(poly):
    if poly.order() > 1:
        raise Exception("We can only solve linear problems at this point.")

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
            steps.append(f"\nSubtract {a} on both sides of the equal sign:")
            steps.append(f'{lhs} - {a} = - {a} + {rhs}')
        else:
            a_pos = a.mult(-1)

            steps.append(f"\nAdd {a_pos} on both sides of the equal sign:")
            steps.append(f'{lhs} + {a_pos} = {a_pos} {rhs}')

        steps.append("\nSimplify both sides:")
        lhs = lhs.subt( a )
        rhs = rhs.subt( a )
        steps.append(f'{lhs} = {rhs}')

    return lhs, rhs, steps

def eliminate_zeroth_order_terms(lhs, rhs):
    steps = []

    b = lhs.get_monomial(0)
    if b.coeff:
        if b.coeff > 0:
            steps.append(f"\nSubtract {b} on both sides of the equal sign:")
            steps.append(f'{lhs} - {b} = {rhs} - {b}')
        else:
            b_pos = b.mult(-1)

            steps.append(f"\nAdd {b_pos} on both sides of the equal sign:")
            steps.append(f'{lhs} + {b_pos} = {rhs} + {b_pos}')
            
        steps.append("\nSimplify both sides:")
        rhs = rhs.subt( b )
        lhs = lhs.subt( b )
        steps.append(f'{lhs} = {rhs}')

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
