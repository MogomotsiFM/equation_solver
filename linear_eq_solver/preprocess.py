"""
Transforms the problem into the ideal format
    Ideal format: Spaces around operators, operands, and brackets
"""

from linear_eq_solver import parse

def preprocess(quest):
    poly = quest.split('=')

    if len(poly) > 2:
        print("Problem not correctly formatted")
        raise Exception("Problem not correctly formatted")
    elif len(poly) == 1:
        poly.append("0")

    exp1 = poly[0].strip().split(' ')
    print("\nSimplify LHS")
    lhs = parse(exp1)
    print("{} = {}".format(lhs, poly[1]))

    exp2 = poly[1].strip().split(' ')
    print("\nSimplify RHS")
    rhs = parse(exp2)
    print("{} = {}".format(lhs, rhs))

    return lhs, rhs
    
