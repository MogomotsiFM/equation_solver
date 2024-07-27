import pytest

from equation_solver import solver
from equation_solver import Monomial
from equation_solver import Polynomial

def test_simple_case():
    # 7x - 2 = 19
    # 7x = 21
    # x = 3
    q = '7x - 2 = 19'

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial(1, 1))
    assert sol[0].get_rhs() == Polynomial(Monomial(3, 0))


def test_not_so_simple_case():
    # 2(4x + 3) + 6x = 15 - 4x
    # 8x + 6 + 6x = 15 - 4x
    # 18x = 9
    # x = 0.5
    q = '2( 4x + 3 ) + 6x = 15 - 4x'

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial( 1, 1))
    assert sol[0].get_rhs() == Polynomial(Monomial(0.5, 0))

def test_solution_does_not_exist():
    # 7x - 2 = 7x
    # 0x = 2
    q = '7x - 2 = 7x'

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial(0, 0))
    assert sol[0].get_rhs() == Polynomial(Monomial(2, 0))

def test_not_so_simple_case_with_multiple_digit_multipliers():
    # 21(- 4x + 3) - 6x = - 31 + 14x
    # -84x + 63 - 6x = - 41 + 14x
    # -104x = -104
    # x = 1
    q = '21( - 4x + 3 ) - 6x = - 41 + 14x'

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial(1, 1))
    assert sol[0].get_rhs() == Polynomial(Monomial(1, 0))

def test_solver_simplifying_both_sides():
    # 2(4x + 3) + 6 = 2(-2x + 10) + 16
    q = "2( 4x + 3 ) + 6 = 2( - 2x + 10 ) + 16"

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial(1, 1))
    assert sol[0].get_rhs() == Polynomial(Monomial(2, 0))

def test_solver_missing_right_hand_side():
    # 2(4x + 3) + 6
    q = "2( 4x + 5 ) + 6"

    sol, _ = solver.solve(q)

    assert sol[0].get_lhs() == Polynomial(Monomial( 1, 1))
    assert sol[0].get_rhs() == Polynomial(Monomial(-2, 0))

def test_solver_simple_steps():
    solution = get_target_solution("test_data/simple_example_solution.txt")

    q = '7x - 2 = 19'
    _, actual = solver.solve(q)

    for a, b in zip(solution, actual):
        assert a == b
    assert actual == solution
    
def test_solver_not_so_simple_steps():
    solution = get_target_solution("test_data/not_so_simple_example_solution.txt")

    q = '21( 4x + 3 ) + 6x - 9 = - 12( - 12x + 10 ) + 12'
    _, actual = solver.solve(q)

    for a, b in zip(solution, actual):
        assert a == b
    assert actual == solution

def test_2nd_solver_simple():
    target = get_target_solution("test_data/second_order_solver_simple.txt")
    
    q = "x^2 - 2x + 1 = 0"

    _, actual = solver.solve(q)

    for a, b in zip(target, actual):
        assert a.strip() == b.strip()
    
def test_solver_missing_closing_bracket_reported():
    with pytest.raises(Exception) as exc:
        # (1 + 6)(x - 3
        q = '( 1 + 6 )( x - 3'

        solver.solve(q)

    assert str(exc.value) == "Could not find matching closing bracket"

# TODO: Use pytest machenisms to load test data.
def get_target_solution(fname):
    solution = None
    # Test data files may not be found depending on wheter pytest 
    # is ran from inside/outside the tests folder.
    try:
        with open(fname, 'r') as f:
            solution = f.readlines()
    except FileNotFoundError:
        fname = "tests/"+fname
        with open(fname, 'r') as f:
            solution = f.readlines()

    filtered = [line.strip() for line in solution if len(line)>1]
    target = list( map(preprocess, filtered) )

    return target

def preprocess(step: str):
    tmp = step.strip()
    if  ':' in tmp:
        return '\n' + step
    else:
        return tmp

