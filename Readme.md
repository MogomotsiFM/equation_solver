### How it works?
* The fundamental data structures are the `Monomial` and `Polynomial` classes.  A `Monomial = ax^n` has a coefficient `a` and an exponent `n`, along with the allowed operations. The composite design pattern is then used to represent a `Polynomial` in terms of the `Monomial` class. This should make it easier to extend to higher-order polynomials. ~~`Polynomial` inheriting from `Monomial` does not seem imminently useful in Python since a list can contain anything. We can do without it.~~ 
    * Permitted operations:
        * Adding one `Monomial` or `Polynomial` to another. It is even possible to add a `Monomial` to 
        a `Polynomial`,
        * Subtracting one `Monomial` or `Polynomial` from another. It is even possible to subtract a `Monomial` from a `Polynomial`,
        * Multiplying a `Monomial` or `Polynomial` by a scalar,
        * Tests for equality,
        * Printing an expressions.
* Steps involved in solving linear problems:
    * **Preprocess** the problem to convert it into a standard format:
        * ~~Spaces around all operators and brackets,~~
        * ~~Unless multiplication is implied in which case the space should be removed,~~
        * Use regular expressions to preprocess the equation,
        * Split the problem into the left and right-hand side expressions,
    * **Parse** the left and right-hand sides expressions individually to simplify them into linear expressions of the form: `ax + b`,
        * For this purpose we use two queue data structures to keep track of the operands and operators separately,
        * Each element of the operands queue is a `Monomial` so it is easier to simplify by applying the methods defined on both the `Monomial` and `Polynomial`,
        * We use recursion to distribute terms, i.e.: `2(3x + 4) = 6x + 8`.
    * **Solve** the simplified problem
        * Steps 
            * Move all the first-order terms to the left-hand side expression, and 
            * Move all the zeroeth order terms to the right-hand side expression,
            * Dividing both sides by the coefficient of the first-order expression.
        * This could have been better represented as a class hierarchy. We could then use the strategy design pattern when implementing solvers for higher-order problems.

### Possible improvements
* Use a tree to keep track of operands and operators instead of two queues.

### How to use it?
* Checkout the code to your local machine: `git clone https://github.com/MogomotsiFM/equation_solver.git equation_solver`
* Change the directory into the source code folder: `cd equation_solver`
* Create a virtual environment: `python -m virtualenv venv`
* Activate the virtual environment: `venv\Scripts\Activate`
* Install requirements: `python -m pip install -r requirements.txt`
* Running tests
    * Open a terminal and change to the root of the application,
    * Type `python -m pytest` at the terminal then press ENTER to run the tests,
* Answering your question
    * Open a terminal and change to the test directory for the test app,
    * Enter your question at the terminal: 
        `python test_app.py 2( 4x + 3 ) + 6x = 24 - 4x` 
    * Press ENTER and the application should respond with the solution.
