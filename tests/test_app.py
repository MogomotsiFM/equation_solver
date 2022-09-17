#!/usr/bin/python

import sys
from context import linear_eq_solver

q = '21( 4x + 3 ) + 6x - 9 = - 12( - 12x + 10 ) + 12'

if len(sys.argv) > 1:
    question = sys.argv[1:]
    
    q = " ".join(question)

print("Question: {}".format(q))

lhs, rhs, steps = linear_eq_solver.solve(q)

print("\n\nSolution: {} = {}".format(lhs, rhs))

print("\n\n\n\nComplete solution\n")
for step in steps:
    print(step)

