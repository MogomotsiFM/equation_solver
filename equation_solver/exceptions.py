from typing import Any

class SolutionDoesNotExistException(Exception):
    value: Any

class FactorDoesNotExistException(Exception):
    value: Any