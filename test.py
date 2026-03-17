import unittest
import math
from calculator import Calculator, HistoryEntry


class TestBasicArithmetic(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_positive(self):
        self.assertEqual(self.calc.add(3, 4), 7)

    def test_add_negative(self):
        self.assertEqual(self.calc.add(-2, -3), -5)

    def test_add_float(self):
        self.assertAlmostEqual(self.calc.add(1.1, 2.2), 3.3)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 4), 6)

    def test_subtract_negative_result(self):
        self.assertEqual(self.calc.subtract(3, 7), -4)

    def test_multiply_positive(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)

    def test_multiply_by_zero(self):
        self.assertEqual(self.calc.multiply(999, 0), 0)

    def test_multiply_negatives(self):
        self.assertEqual(self.calc.multiply(-3, -4), 12)

    def test_divide_normal(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_float_result(self):
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333333333)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)


class TestAdvancedMath(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_power_integer(self):
        self.assertEqual(self.calc.power(2, 10), 1024)

    def test_power_fractional_exp(self):
        self.assertAlmostEqual(self.calc.power(9, 0.5), 3.0)

    def test_power_zero_exp(self):
        self.assertEqual(self.calc.power(100, 0), 1)

    def test_sqrt_positive(self):
        self.assertAlmostEqual(self.calc.sqrt(16), 4.0)

    def test_sqrt_zero(self):
        self.assertEqual(self.calc.sqrt(0), 0)

    def test_sqrt_negative(self):
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

    def test_nth_root_cube(self):
        self.assertAlmostEqual(self.calc.nth_root(27, 3), 3.0)

    def test_nth_root_square(self):
        self.assertAlmostEqual(self.calc.nth_root(25, 2), 5.0)

    def test_nth_root_negative_odd(self):
        self.assertAlmostEqual(self.calc.nth_root(-8, 3), -2.0)

    def test_nth_root_negative_even(self):
        with self.assertRaises(ValueError):
            self.calc.nth_root(-4, 2)

    def test_nth_root_zero_n(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.nth_root(8, 0)

    def test_log10_normal(self):
        self.assertAlmostEqual(self.calc.log10(100), 2.0)

    def test_log10_one(self):
        self.assertEqual(self.calc.log10(1), 0)

    def test_log10_zero(self):
        with self.assertRaises(ValueError):
            self.calc.log10(0)

    def test_log10_negative(self):
        with self.assertRaises(ValueError):
            self.calc.log10(-5)

    def test_ln_e(self):
        self.assertAlmostEqual(self.calc.ln(math.e), 1.0)

    def test_ln_one(self):
        self.assertEqual(self.calc.ln(1), 0)

    def test_ln_negative(self):
        with self.assertRaises(ValueError):
            self.calc.ln(-1)

    def test_factorial_zero(self):
        self.assertEqual(self.calc.factorial(0), 1)

    def test_factorial_positive(self):
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_whole_float(self):
        self.assertEqual(self.calc.factorial(4.0), 24)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_float_noninteger(self):
        with self.assertRaises(ValueError):
            self.calc.factorial(3.5)


class TestTrigonometry(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_sin_zero(self):
        self.assertAlmostEqual(self.calc.sin(0), 0.0)

    def test_sin_pi_half(self):
        self.assertAlmostEqual(self.calc.sin(math.pi / 2), 1.0)

    def test_cos_zero(self):
        self.assertAlmostEqual(self.calc.cos(0), 1.0)

    def test_cos_pi(self):
        self.assertAlmostEqual(self.calc.cos(math.pi), -1.0)

    def test_tan_zero(self):
        self.assertAlmostEqual(self.calc.tan(0), 0.0)

    def test_tan_pi_quarter(self):
        self.assertAlmostEqual(self.calc.tan(math.pi / 4), 1.0)

    def test_asin_valid(self):
        self.assertAlmostEqual(self.calc.asin(1.0), math.pi / 2)

    def test_asin_zero(self):
        self.assertAlmostEqual(self.calc.asin(0), 0.0)

    def test_asin_out_of_domain(self):
        with self.assertRaises(ValueError):
            self.calc.asin(1.5)

    def test_acos_valid(self):
        self.assertAlmostEqual(self.calc.acos(1.0), 0.0)

    def test_acos_out_of_domain(self):
        with self.assertRaises(ValueError):
            self.calc.acos(-2.0)

    def test_atan(self):
        self.assertAlmostEqual(self.calc.atan(1.0), math.pi / 4)

    def test_to_degrees(self):
        self.assertAlmostEqual(self.calc.to_degrees(math.pi), 180.0)

    def test_to_radians(self):
        self.assertAlmostEqual(self.calc.to_radians(180), math.pi)

    def test_degrees_radians_roundtrip(self):
        original = 45.0
        converted = self.calc.to_radians(original)
        back = self.calc.to_degrees(converted)
        self.assertAlmostEqual(back, original)


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_initial_memory_is_zero(self):
        self.assertEqual(self.calc.memory_recall(), 0.0)

    def test_memory_store_and_recall(self):
        self.calc.memory_store(42.5)
        self.assertEqual(self.calc.memory_recall(), 42.5)

    def test_memory_clear(self):
        self.calc.memory_store(100)
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory_recall(), 0.0)

    def test_memory_add(self):
        self.calc.memory_store(10)
        self.calc.memory_add(5)
        self.assertEqual(self.calc.memory_recall(), 15)

    def test_memory_add_multiple(self):
        self.calc.memory_add(3)
        self.calc.memory_add(7)
        self.calc.memory_add(10)
        self.assertEqual(self.calc.memory_recall(), 20)

    def test_memory_does_not_affect_history(self):
        self.calc.memory_store(99)
        self.calc.memory_recall()
        self.calc.memory_clear()
        self.calc.memory_add(1)
        self.assertEqual(len(self.calc.get_history()), 0)


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_history_initially_empty(self):
        self.assertEqual(self.calc.get_history(), [])

    def test_history_records_operations(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        self.assertEqual(len(self.calc.get_history()), 2)

    def test_history_entry_values(self):
        self.calc.add(5, 6)
        entry = self.calc.get_history()[0]
        self.assertIsInstance(entry, HistoryEntry)
        self.assertEqual(entry.result, 11)

    def test_history_clear(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(self.calc.get_history(), [])

    def test_last_result_empty(self):
        self.assertIsNone(self.calc.last_result())

    def test_last_result_after_ops(self):
        self.calc.add(10, 5)
        self.calc.multiply(2, 3)
        self.assertEqual(self.calc.last_result(), 6)

    def test_get_history_returns_copy(self):
        self.calc.add(1, 2)
        history_copy = self.calc.get_history()
        history_copy.clear()
        self.assertEqual(len(self.calc.get_history()), 1)


class TestConstants(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_pi_value(self):
        self.assertAlmostEqual(self.calc.PI, 3.141592653589793)

    def test_e_value(self):
        self.assertAlmostEqual(self.calc.E, 2.718281828459045)

    def test_phi_value(self):
        self.assertAlmostEqual(self.calc.PHI, 1.618033988749895)


class TestUtility(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_percentage(self):
        self.assertEqual(self.calc.percentage(200, 50), 100)

    def test_percentage_zero(self):
        self.assertEqual(self.calc.percentage(500, 0), 0)

    def test_absolute_value_positive(self):
        self.assertEqual(self.calc.absolute_value(7), 7)

    def test_absolute_value_negative(self):
        self.assertEqual(self.calc.absolute_value(-7), 7)

    def test_absolute_value_zero(self):
        self.assertEqual(self.calc.absolute_value(0), 0)

    def test_reciprocal(self):
        self.assertEqual(self.calc.reciprocal(2), 0.5)

    def test_reciprocal_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.reciprocal(0)

    def test_modulo_normal(self):
        self.assertEqual(self.calc.modulo(10, 3), 1)

    def test_modulo_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.modulo(5, 0)

    def test_modulo_float(self):
        self.assertAlmostEqual(self.calc.modulo(5.5, 2.0), 1.5)


if __name__ == "__main__":
    unittest.main()
