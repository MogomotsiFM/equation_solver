"""
Solves linear equations
"""

from linear_eq_solver import preprocess, second_order_eq_solver
from linear_eq_solver import parse
from linear_eq_solver import linear_solver
from linear_eq_solver import second_order_eq_solver

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

    lhs, rhs, substeps = linear_solver.LinearSolver().solve(lhs, rhs)
    #sol, _, substeps = second_order_eq_solver.SecondOrderEqSolver().solve(lhs, rhs)
    steps.extend(substeps)

    #if len(sol) == 2:
    #    lhs = sol[0]
    #    rhs = sol[1]
    

    steps.append("\nSolution:")
    steps.append(f'{lhs} = {rhs}')
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
