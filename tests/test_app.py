#!/usr/bin/python

import sys
from context import linear_eq_solver

q = '2( 4x + 3 ) + 6x = 15 - 4x'

if len(sys.argv) > 1:
    question = sys.argv[1:]
    for t in question:
        print(t)
    q = " ".join(question)

print("Question: ".format(q))

lhs, rhs = linear_eq_solver.solve(q)

print("\n\nSolution: {} = {}".format(lhs, rhs))

