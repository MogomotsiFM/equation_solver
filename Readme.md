### How it works?
* The fundamental data structures are the `Monomial` and `Polynomial` classes.  A `Monomial = ax^n` has a coefficient `a` and an exponent `n`, along with the allowed operations. The composite design pattern is then used to represent a `Polynomial` in terms of the `Monomial` class. This should make it easier to extend to higher order polynomials. ~~`Polynomial` inheriting from `Monomial` does not seem imminently useful in Python since a list can contain anything. We can do without it.~~ 
    * Permited operations:
        * Adding one `Monomial` or `Polynomial` to another. It is even possible to add a `Monomial` to 
        a `Polynomial`,
        * Subracting one `Monomial` or `Polynomial` from another. It is even possible to subtract a `Monomial` from a `Polynomial`,
        * Multiplying an `Monomial` or `Polynomial` by a scalar,
        * Tests for equality,
        * Printing an expressions.
* Steps involved in solving linear problems:
    * **Preprocess** the problem to convert it into a standard format:
        * Spaces around all operators and brackets,
        * Unless multiplication is implied in which case the space should be removed,
        * Split the problem into the left and right hand side expressions,
    * **Parse** the left and right hand sides expressions individualy to simplify them into linear expressions of the form: `ax + b`,
        * For this purpose we use two queue data structures to keep track of the operands and operators separately,
        * Each element of the operands queue is an `Monomial` and so it is easier to simplify by applying the methods defined on both the `Monomial` and `Polynomial`,
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