"""
Transforms the problem into the ideal format
    Ideal format: Spaces around operators, operands, and brackets
                  unless multiplication is implied.
"""

from linear_eq_solver import parse

def preprocess(quest):
    # A list of steps taken in solving the problem
    steps = list()

    poly = quest.split('=')

    if len(poly) > 2:
        steps.append("\nProblem not correctly formatted")
        
        raise Exception("Problem not correctly formatted")
    elif len(poly) == 1:
        poly.append("0")

    lhs_exp = poly[0].strip().split(' ')
    rhs_exp = poly[1].strip().split(' ')

    steps.append("\nSimplify LHS:")
    lhs, lhs_sub_steps = parse(lhs_exp)
    steps.extend(append_rhs(lhs_sub_steps, poly[1]))
    
    steps.append("\n{} = {}".format(lhs, poly[1]))

    steps.append("\nSimplify RHS:")
    rhs, rhs_sub_steps = parse(rhs_exp)
    steps.extend(append_lhs(rhs_sub_steps, lhs))

    return lhs, rhs, steps
    
def append_lhs(rhs_substeps: list, lhs_expr):
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
    # Note that we do not generate equations if a step ends with a colon
    # This is because those steps highlight the maths concept used
    # This is why we need this hidden functions
    def append_rhs_to_single_step(substep: str, rhs_expr):
        if substep[-1] == ':':
            return substep
        return substep + ' = ' + rhs_expr

    steps = map(lambda s: append_rhs_to_single_step(s, rhs_expr), lhs_substeps)
    
    return list(steps)