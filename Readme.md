### How it works?
* The fundamental data structure is an `Expression`. An `Expression` is a first order polynomial represented as two numbers and a set of permited operations.
    * Permited operations:
        * Adding one expression to another,
        * Subracting one expression from another,
        * Multiplying an expression by a scalar,
        * Test for equality,
        * Printing an expression.
    * A better alternative could probably have been to represent a `Monomial = ax^n` as a coefficient `a` and an exponent `n`, along with the allowed operations. We could then use the composite design pattern to represent an `Expression` in terms of the `Monomial` class. This would make it easier to extend to higher order polynomials.
* Steps involved in solving linear problems:
    * **Preprocess** the problem to convert it into a standard format:
        * Spaces around all operators and brackets,
        * Unless multiplication is implied in which case the space should be removed,
        * Split the problem into the left and right hand side expressions,
    * **Parse** the left and right hand sides expressions individualy to simplify them into linear expressions of the form: `ax + b`,
        * For this purpose we use two queue data structures to keep track of the operands and operators separately,
        * Each element of the operands queue is an `Expression` and so it is easier to simplify by applying the rules defined on an `Expression`,
        * We use recursion to distribute terms, i.e.: `2(3x + 4) = 6x + 8`.
    * **Solve** the simplified problem
        * Steps 
            * Move all the first order terms to the left hand side expression, and 
            * Move all the zeroeth order terms to the right hand side expression,
            * Deviding both sides by the coefficient of the first order expression.
        * This could have been better represented as a class hierachy. We could then use the strategy design pattern when implementing solvers for higher order problems.


### How to use it?
* Checkout the code to your local machine: `git clone url_to_root_folder`
* Running tests
    * Install `pytest`: `python3 -m pip install pytest`
    * Open a terminal and change to the root of the application,
    * Type `pytest` at the terminal then press ENTER to run the tests,
* Answering your own question
    * Open a terminal and change to the test directory for the test app,
    * Enter your question at the terminal: 
        `python3 test_app.py 2( 4x + 3 ) + 6x = 24 - 4x` 
    * Ensure that there are spaces around the operators and parenthesis, unless multiplication is implied,
    * Press ENTER and the application should respond with the solution.