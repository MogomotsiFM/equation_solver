"""
Solves linear equations
"""

from linear_eq_solver import preprocess
from linear_eq_solver import parse
from linear_eq_solver import linear_solver
from linear_eq_solver import quadratic_eq_solver

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

    sol = None
    if max(lhs.order(), rhs.order()) == 1:
        print("First order problem")
        sol, substeps = linear_solver.LinearSolver().solve(lhs, rhs)
        
        steps.extend(substeps)
    elif max(lhs.order(), rhs.order()) == 2:
        print("Second order problem")
        sol, substeps = quadratic_eq_solver.QuadraticEqSolver().solve(lhs, rhs)

        steps.extend(substeps)
    else:
        raise Exception("Trying to solve order 3 or more problem, good luck with that")

    steps.append("\nSolution:")
    solution = [f'{a.get_lhs()} = {a.get_rhs()}' for a in sol]
    steps.append('    OR    '.join(solution))

    return sol, steps

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
