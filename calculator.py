import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HistoryEntry:
    expression: str
    result: float


class Calculator:
    def __init__(self):
        self._memory: float = 0.0
        self._history: list = []

    # ------------------------------------------------------------------ #
    # Internal helper                                                      #
    # ------------------------------------------------------------------ #

    def _record(self, expression: str, result: float) -> float:
        self._history.append(HistoryEntry(expression, result))
        return result

    # ------------------------------------------------------------------ #
    # Constants                                                            #
    # ------------------------------------------------------------------ #

    @property
    def PI(self) -> float:
        return math.pi

    @property
    def E(self) -> float:
        return math.e

    @property
    def PHI(self) -> float:
        return (1 + math.sqrt(5)) / 2

    # ------------------------------------------------------------------ #
    # Basic Arithmetic                                                     #
    # ------------------------------------------------------------------ #

    def add(self, a: float, b: float) -> float:
        result = a + b
        return self._record(f"{a} + {b} = {result}", result)

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        return self._record(f"{a} - {b} = {result}", result)

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        return self._record(f"{a} * {b} = {result}", result)

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a / b
        return self._record(f"{a} / {b} = {result}", result)

    # ------------------------------------------------------------------ #
    # Advanced Math                                                        #
    # ------------------------------------------------------------------ #

    def power(self, base: float, exp: float) -> float:
        result = base ** exp
        return self._record(f"{base} ^ {exp} = {result}", result)

    def sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Cannot take sqrt of a negative number")
        result = math.sqrt(x)
        return self._record(f"sqrt({x}) = {result}", result)

    def nth_root(self, x: float, n: float) -> float:
        if n == 0:
            raise ZeroDivisionError("Root degree cannot be zero")
        if x < 0:
            if isinstance(n, int) or (isinstance(n, float) and n.is_integer()):
                n_int = int(n)
                if n_int % 2 == 0:
                    raise ValueError("Cannot take even root of a negative number")
                result = -(abs(x) ** (1 / n_int))
            else:
                raise ValueError("Cannot take non-integer root of a negative number")
        else:
            result = x ** (1 / n)
        return self._record(f"nthroot({x}, {n}) = {result}", result)

    def log10(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Logarithm requires a positive number")
        result = math.log10(x)
        return self._record(f"log10({x}) = {result}", result)

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Natural log requires a positive number")
        result = math.log(x)
        return self._record(f"ln({x}) = {result}", result)

    def factorial(self, n) -> float:
        if isinstance(n, float):
            if not n.is_integer():
                raise ValueError("Factorial requires a non-negative integer")
            n = int(n)
        if not isinstance(n, int):
            raise TypeError("Factorial requires an integer or whole-number float")
        if n < 0:
            raise ValueError("Factorial of a negative number is undefined")
        result = math.factorial(n)
        return self._record(f"{n}! = {result}", float(result))

    # ------------------------------------------------------------------ #
    # Trigonometry (angles in radians)                                    #
    # ------------------------------------------------------------------ #

    def sin(self, angle_rad: float) -> float:
        result = math.sin(angle_rad)
        return self._record(f"sin({angle_rad}) = {result}", result)

    def cos(self, angle_rad: float) -> float:
        result = math.cos(angle_rad)
        return self._record(f"cos({angle_rad}) = {result}", result)

    def tan(self, angle_rad: float) -> float:
        # math.tan returns a very large float near pi/2 + n*pi — no special case needed
        result = math.tan(angle_rad)
        return self._record(f"tan({angle_rad}) = {result}", result)

    def asin(self, x: float) -> float:
        if not -1 <= x <= 1:
            raise ValueError(f"asin domain is [-1, 1], got {x}")
        result = math.asin(x)
        return self._record(f"asin({x}) = {result}", result)

    def acos(self, x: float) -> float:
        if not -1 <= x <= 1:
            raise ValueError(f"acos domain is [-1, 1], got {x}")
        result = math.acos(x)
        return self._record(f"acos({x}) = {result}", result)

    def atan(self, x: float) -> float:
        result = math.atan(x)
        return self._record(f"atan({x}) = {result}", result)

    def to_degrees(self, angle_rad: float) -> float:
        result = math.degrees(angle_rad)
        return self._record(f"to_degrees({angle_rad}) = {result}", result)

    def to_radians(self, angle_deg: float) -> float:
        result = math.radians(angle_deg)
        return self._record(f"to_radians({angle_deg}) = {result}", result)

    # ------------------------------------------------------------------ #
    # Memory                                                               #
    # ------------------------------------------------------------------ #

    def memory_store(self, value: float) -> None:
        self._memory = value

    def memory_recall(self) -> float:
        return self._memory

    def memory_clear(self) -> None:
        self._memory = 0.0

    def memory_add(self, value: float) -> None:
        self._memory += value

    # ------------------------------------------------------------------ #
    # History                                                              #
    # ------------------------------------------------------------------ #

    def get_history(self) -> list:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()

    def last_result(self) -> Optional[float]:
        if not self._history:
            return None
        return self._history[-1].result

    # ------------------------------------------------------------------ #
    # Utility                                                              #
    # ------------------------------------------------------------------ #

    def percentage(self, value: float, percent: float) -> float:
        result = (value * percent) / 100
        return self._record(f"{percent}% of {value} = {result}", result)

    def absolute_value(self, x: float) -> float:
        result = abs(x)
        return self._record(f"abs({x}) = {result}", result)

    def reciprocal(self, x: float) -> float:
        if x == 0:
            raise ZeroDivisionError("Cannot take reciprocal of zero")
        result = 1 / x
        return self._record(f"1/{x} = {result}", result)

    def modulo(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot modulo by zero")
        result = a % b
        return self._record(f"{a} % {b} = {result}", result)
