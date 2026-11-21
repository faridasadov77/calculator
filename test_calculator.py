"""Tests for calculator module."""
import pytest
from calculator import Calculator, parse_number, validate_operator, parse_expression, evaluate_expression


class TestCalculator:
    """Test cases for Calculator class."""

    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0
        assert self.calc.add(1.5, 2.5) == 4.0

    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(0, 5) == -5
        assert self.calc.subtract(-2, -3) == 1
        assert self.calc.subtract(3.5, 1.2) == 2.3

    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(0, 100) == 0
        assert self.calc.multiply(1.5, 2) == 3.0

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
        assert self.calc.divide(-6, 2) == -3
        assert self.calc.divide(0, 5) == 0

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(5, 0)


class TestParseNumber:
    """Test cases for parse_number function."""

    def test_valid_integers(self):
        assert parse_number("5") == 5.0
        assert parse_number("-10") == -10.0
        assert parse_number("0") == 0.0

    def test_valid_floats(self):
        assert parse_number("3.14") == 3.14
        assert parse_number("-2.5") == -2.5
        assert parse_number("0.0") == 0.0

    def test_scientific_notation(self):
        assert parse_number("1e5") == 100000.0
        assert parse_number("2.5e-3") == 0.0025

    def test_whitespace_handling(self):
        assert parse_number("  42  ") == 42.0
        assert parse_number("\t3.14\n") == 3.14

    def test_empty_string(self):
        with pytest.raises(ValueError, match="Boş sayı girişi"):
            parse_number("")
        with pytest.raises(ValueError, match="Boş sayı girişi"):
            parse_number("   ")

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_number("abc")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_number("5.2.3")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_number("5+")

    def test_nan_rejected(self):
        with pytest.raises(ValueError, match="NaN"):
            parse_number("nan")
        with pytest.raises(ValueError, match="NaN"):
            parse_number("NaN")

    def test_infinity_rejected(self):
        with pytest.raises(ValueError, match="Sonsuz"):
            parse_number("inf")
        with pytest.raises(ValueError, match="Sonsuz"):
            parse_number("-inf")
        with pytest.raises(ValueError, match="Sonsuz"):
            parse_number("infinity")


class TestValidateOperator:
    """Test cases for validate_operator function."""

    def test_valid_operators(self):
        assert validate_operator("+") == "+"
        assert validate_operator("-") == "-"
        assert validate_operator("*") == "*"
        assert validate_operator("/") == "/"

    def test_invalid_operators(self):
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            validate_operator("%")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            validate_operator("^")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            validate_operator("x")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            validate_operator("")


class TestParseExpression:
    """Test cases for parse_expression function (backward compatibility)."""

    def test_valid_expressions(self):
        # Space-separated (original format)
        assert parse_expression("5 + 3") == (5.0, "+", 3.0)
        assert parse_expression("10 - 4") == (10.0, "-", 4.0)
        assert parse_expression("6 * 7") == (6.0, "*", 7.0)
        assert parse_expression("20 / 4") == (20.0, "/", 4.0)
        assert parse_expression("  2.5  +  1.5  ") == (2.5, "+", 1.5)
        assert parse_expression("-5 * -2") == (-5.0, "*", -2.0)
        
        # No spaces
        assert parse_expression("5+3") == (5.0, "+", 3.0)
        assert parse_expression("10-4") == (10.0, "-", 4.0)
        assert parse_expression("6*7") == (6.0, "*", 7.0)
        assert parse_expression("20/4") == (20.0, "/", 4.0)
        
        # Partial spaces
        assert parse_expression("5 +3") == (5.0, "+", 3.0)
        assert parse_expression("5+ 3") == (5.0, "+", 3.0)
        assert parse_expression("10 -4") == (10.0, "-", 4.0)
        assert parse_expression("10- 4") == (10.0, "-", 4.0)
        
        # Negative numbers with various formats
        assert parse_expression("-5+3") == (-5.0, "+", 3.0)
        assert parse_expression("5+-3") == (5.0, "+", -3.0)
        assert parse_expression("-5+-3") == (-5.0, "+", -3.0)
        assert parse_expression("5.5*-2.3") == (5.5, "*", -2.3)
        assert parse_expression("-10/-2") == (-10.0, "/", -2.0)

    def test_empty_expression(self):
        with pytest.raises(ValueError, match="Boş ifade"):
            parse_expression("")
        with pytest.raises(ValueError, match="Boş ifade"):
            parse_expression("   ")

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Operatör bulunamadı"):
            parse_expression("5")
        with pytest.raises(ValueError, match="Her iki tarafında da sayı"):
            parse_expression("5+")
        with pytest.raises(ValueError, match="Her iki tarafında da sayı"):
            parse_expression("+3")
        with pytest.raises(ValueError, match="Operatör bulunamadı"):
            parse_expression("5 3")

    def test_invalid_number_in_expression(self):
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_expression("abc + 3")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_expression("5 + xyz")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_expression("5.2.3 + 1")

    def test_invalid_operator_in_expression(self):
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            parse_expression("5 % 3")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            parse_expression("5 ^ 3")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            parse_expression("5 x 3")

    def test_nan_in_expression(self):
        with pytest.raises(ValueError, match="NaN"):
            parse_expression("nan + 3")

    def test_infinity_in_expression(self):
        with pytest.raises(ValueError, match="Sonsuz"):
            parse_expression("inf + 3")

    def test_multiple_operators_first_top_level(self):
        # parse_expression returns first top-level operator for backward compatibility
        # but the full expression is evaluated correctly by evaluate_expression
        a, op, b = parse_expression("5+3-2")
        assert op == "+"
        assert a == 5.0
        assert b == 1.0  # right side "3-2" is evaluated fully
        
        a, op, b = parse_expression("10-5*2")
        assert op == "-"
        assert a == 10.0
        assert b == 10.0  # right side "5*2" is evaluated fully


class TestEvaluateExpression:
    """Test cases for evaluate_expression function (full expression evaluation)."""

    def test_basic_operations(self):
        assert evaluate_expression("5 + 3") == 8.0
        assert evaluate_expression("10 - 4") == 6.0
        assert evaluate_expression("6 * 7") == 42.0
        assert evaluate_expression("20 / 4") == 5.0

    def test_operator_precedence(self):
        # Multiplication/division before addition/subtraction
        assert evaluate_expression("5 + 3 * 2") == 11.0  # 5 + (3*2) = 11
        assert evaluate_expression("10 - 4 / 2") == 8.0  # 10 - (4/2) = 8
        assert evaluate_expression("3 * 4 + 5") == 17.0  # (3*4) + 5 = 17
        assert evaluate_expression("20 / 4 - 2") == 3.0  # (20/4) - 2 = 3

    def test_left_to_right_associativity(self):
        # Same precedence: left to right
        assert evaluate_expression("10 - 5 - 2") == 3.0  # (10-5)-2 = 3
        assert evaluate_expression("20 / 4 / 2") == 2.5  # (20/4)/2 = 2.5
        assert evaluate_expression("5 + 3 + 2") == 10.0  # (5+3)+2 = 10
        assert evaluate_expression("6 * 7 / 2") == 21.0  # (6*7)/2 = 21

    def test_parentheses(self):
        assert evaluate_expression("(5 + 3) * 2") == 16.0
        assert evaluate_expression("10 - (4 / 2)") == 8.0
        assert evaluate_expression("(3 + 2) * (4 - 1)") == 15.0
        assert evaluate_expression("((2 + 3) * 4)") == 20.0
        assert evaluate_expression("5 * (3 + 2)") == 25.0

    def test_negative_numbers(self):
        assert evaluate_expression("-5 + 3") == -2.0
        assert evaluate_expression("5 + -3") == 2.0
        assert evaluate_expression("-5 * -2") == 10.0
        assert evaluate_expression("5 * -2") == -10.0
        assert evaluate_expression("-10 / -2") == 5.0
        assert evaluate_expression("(-5) + 3") == -2.0
        assert evaluate_expression("5 * (-2 + 1)") == -5.0

    def test_decimals(self):
        assert evaluate_expression("2.5 + 1.5") == 4.0
        assert evaluate_expression("3.14 * 2") == 6.28
        assert evaluate_expression("10 / 4") == 2.5
        assert evaluate_expression("0.1 + 0.2") == pytest.approx(0.3)

    def test_flexible_spacing(self):
        assert evaluate_expression("5+3") == 8.0
        assert evaluate_expression("5 +3") == 8.0
        assert evaluate_expression("5+ 3") == 8.0
        assert evaluate_expression("  5  +  3  ") == 8.0
        assert evaluate_expression("(5+3)*2") == 16.0

    def test_complex_expressions(self):
        assert evaluate_expression("2 + 3 * 4 - 5 / 2") == 11.5  # 2 + 12 - 2.5 = 11.5
        assert evaluate_expression("(2 + 3) * (4 - 1) / 2") == 7.5
        assert evaluate_expression("10 - 2 * 3 + 4 / 2") == 6.0  # 10 - 6 + 2 = 6

    def test_empty_expression(self):
        with pytest.raises(ValueError, match="Boş ifade"):
            evaluate_expression("")
        with pytest.raises(ValueError, match="Boş ifade"):
            evaluate_expression("   ")

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Geçersiz karakter"):
            evaluate_expression("5 % 3")
        with pytest.raises(ValueError, match="Geçersiz karakter"):
            evaluate_expression("5 ^ 3")
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression("(5 + 3")
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression("5 + 3)")
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression(")5 + 3(")

    def test_invalid_number(self):
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            evaluate_expression("abc + 3")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            evaluate_expression("5 + xyz")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            evaluate_expression("5.2.3 + 1")

    def test_nan_rejected(self):
        with pytest.raises(ValueError, match="NaN"):
            evaluate_expression("nan + 3")

    def test_infinity_rejected(self):
        with pytest.raises(ValueError, match="Sonsuz"):
            evaluate_expression("inf + 3")
        with pytest.raises(ValueError, match="Sonsuz"):
            evaluate_expression("5 / 0")  # Division by zero gives infinity

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            evaluate_expression("5 / 0")

    def test_exponentiation(self):
        assert evaluate_expression("2 ** 3") == 8.0
        assert evaluate_expression("5 ** 2") == 25.0
        assert evaluate_expression("2 ** 0.5") == pytest.approx(1.41421356)
        assert evaluate_expression("10 ** -1") == 0.1
        assert evaluate_expression("(-2) ** 3") == -8.0

    def test_exponentiation_precedence(self):
        # ** has higher precedence than * and /
        assert evaluate_expression("2 * 3 ** 2") == 18.0  # 2 * (3**2) = 18
        assert evaluate_expression("2 ** 3 * 4") == 32.0  # (2**3) * 4 = 32
        assert evaluate_expression("2 + 3 ** 2") == 11.0  # 2 + (3**2) = 11
        assert evaluate_expression("2 ** 3 ** 2") == 512.0  # Right-associative: 2 ** (3**2) = 2**9 = 512

    def test_sqrt(self):
        assert evaluate_expression("sqrt(25)") == 5.0
        assert evaluate_expression("sqrt(2)") == pytest.approx(1.41421356)
        assert evaluate_expression("sqrt(0)") == 0.0
        assert evaluate_expression("sqrt(1)") == 1.0

    def test_sqrt_negative(self):
        with pytest.raises(ValueError, match="Karekök negatif"):
            evaluate_expression("sqrt(-1)")
        with pytest.raises(ValueError, match="Karekök negatif"):
            evaluate_expression("sqrt(-25)")

    def test_trig_functions(self):
        assert evaluate_expression("sin(0)") == 0.0
        assert evaluate_expression("cos(0)") == 1.0
        assert evaluate_expression("tan(0)") == 0.0
        assert evaluate_expression("sin(pi/2)") == pytest.approx(1.0)
        assert evaluate_expression("cos(pi)") == pytest.approx(-1.0)

    def test_log_functions(self):
        assert evaluate_expression("log(100)") == 2.0
        assert evaluate_expression("log(10)") == 1.0
        assert evaluate_expression("log(1)") == 0.0
        assert evaluate_expression("ln(e)") == pytest.approx(1.0)
        assert evaluate_expression("ln(1)") == 0.0
        assert evaluate_expression("ln(e**2)") == pytest.approx(2.0)

    def test_log_invalid(self):
        with pytest.raises(ValueError, match="Logaritma"):
            evaluate_expression("log(0)")
        with pytest.raises(ValueError, match="Logaritma"):
            evaluate_expression("log(-1)")
        with pytest.raises(ValueError, match="Doğal logaritma"):
            evaluate_expression("ln(0)")
        with pytest.raises(ValueError, match="Doğal logaritma"):
            evaluate_expression("ln(-1)")

    def test_constants(self):
        assert evaluate_expression("pi") == pytest.approx(math.pi)
        assert evaluate_expression("e") == pytest.approx(math.e)
        assert evaluate_expression("2 * pi") == pytest.approx(2 * math.pi)
        assert evaluate_expression("e ** 2") == pytest.approx(math.e ** 2)

    def test_complex_expressions_with_new_features(self):
        assert evaluate_expression("sqrt(25) + 3 * 2") == 11.0
        assert evaluate_expression("(5 + 3) * 2 ** 2") == 32.0
        assert evaluate_expression("sin(pi/2) + cos(0)") == 2.0
        assert evaluate_expression("log(100) + ln(e)") == 3.0
        assert evaluate_expression("sqrt(2 ** 4)") == 4.0
        assert evaluate_expression("2 ** 3 ** 2") == 512.0  # Right associative