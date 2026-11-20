"""Tests for calculator module."""
import pytest
from calculator import Calculator, parse_number, validate_operator, parse_expression


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
    """Test cases for parse_expression function."""

    def test_valid_expressions(self):
        assert parse_expression("5 + 3") == (5.0, "+", 3.0)
        assert parse_expression("10 - 4") == (10.0, "-", 4.0)
        assert parse_expression("6 * 7") == (6.0, "*", 7.0)
        assert parse_expression("20 / 4") == (20.0, "/", 4.0)
        assert parse_expression("  2.5  +  1.5  ") == (2.5, "+", 1.5)
        assert parse_expression("-5 * -2") == (-5.0, "*", -2.0)

    def test_empty_expression(self):
        with pytest.raises(ValueError, match="Boş ifade"):
            parse_expression("")
        with pytest.raises(ValueError, match="Boş ifade"):
            parse_expression("   ")

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Format: sayı operatör sayı"):
            parse_expression("5 +")
        with pytest.raises(ValueError, match="Format: sayı operatör sayı"):
            parse_expression("5 + 3 2")
        with pytest.raises(ValueError, match="Format: sayı operatör sayı"):
            parse_expression("5")

    def test_invalid_number_in_expression(self):
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_expression("abc + 3")
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            parse_expression("5 + xyz")

    def test_invalid_operator_in_expression(self):
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            parse_expression("5 % 3")
        with pytest.raises(ValueError, match="Geçersiz operatör"):
            parse_expression("5 ^ 3")

    def test_nan_in_expression(self):
        with pytest.raises(ValueError, match="NaN"):
            parse_expression("nan + 3")

    def test_infinity_in_expression(self):
        with pytest.raises(ValueError, match="Sonsuz"):
            parse_expression("inf + 3")