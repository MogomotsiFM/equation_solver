"""
Transforms the problem into the ideal format
    Ideal format: Spaces around operators, operands, and brackets
                  unless multiplication is implied.
"""
def preprocess(quest):
    poly = quest.split('=')

    if len(poly) > 2:
        raise Exception("Problem not correctly formatted")
    elif len(poly) == 1:
        poly.append("0")

    lhs_exp = poly[0].strip().split(' ')
    rhs_exp = poly[1].strip().split(' ')

    return lhs_exp, rhs_exp
    