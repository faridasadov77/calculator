"""Tests for strict syntax validation in calculator module."""
import re
import pytest
from calculator import evaluate_expression


class TestStrictSyntax:
    """Test cases for strict syntax validation."""

    def test_functions_without_parentheses(self):
        """Test that functions without parentheses raise appropriate errors."""
        # Functions without parentheses should raise specific error
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("sqrt 25 + 1")
        
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("sin pi / 2")
        
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("cos 0")
        
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("tan pi")
        
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("log 100")
        
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("ln e")

    def test_operands_and_operators_not_alternating(self):
        """Test that operands and operators that don't alternate raise appropriate errors."""
        # Two numbers in a row
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("5 3 -")
        
        # Two operators in a row (except for valid cases like negative numbers)
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("5 + * 3")
        
        # Operator at start (except unary minus)
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("+ 5 3")
        
        # Operator at end
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("5 3 +")
        
        # Multiple consecutive numbers
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("1 2 3 +")
        
        # Invalid sequence with scientific notation
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("1e 5")

    def test_valid_expressions_still_work(self):
        """Test that valid expressions continue to work correctly."""
        # Basic operations
        assert evaluate_expression("5 + 3") == 8.0
        assert evaluate_expression("10 - 4") == 6.0
        assert evaluate_expression("6 * 7") == 42.0
        assert evaluate_expression("20 / 4") == 5.0
        
        # Functions with parentheses (should work)
        assert evaluate_expression("sqrt(25)") == 5.0
        assert evaluate_expression("sin(pi/2)") == pytest.approx(1.0)
        assert evaluate_expression("cos(0)") == 1.0
        assert evaluate_expression("log(100)") == 2.0
        assert evaluate_expression("ln(e)") == pytest.approx(1.0)
        
        # Complex expressions
        assert evaluate_expression("(5 + 3) * 2") == 16.0
        assert evaluate_expression("sqrt(25) + 3 * 2") == 11.0
        assert evaluate_expression("sin(pi/2) + cos(0)") == 2.0
        
        # Negative numbers (should work)
        assert evaluate_expression("-5 + 3") == -2.0
        assert evaluate_expression("5 + -3") == 2.0
        assert evaluate_expression("-5 * -2") == 10.0

    def test_function_name_without_argument(self):
        """A function name that ends the input or is followed by an operator is rejected."""
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("sqrt")

        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("2 * sin")

        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("cos + 1")

    def test_mixed_invalid_cases(self):
        """Test mixed invalid cases that should raise errors."""
        # Function without parentheses followed by invalid operator sequence
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("sqrt 25 3")
        
        # Valid function call followed by invalid sequence
        with pytest.raises(ValueError, match="Geçersiz ifade"):
            evaluate_expression("sqrt(25) 3 +")
        
        # Multiple function calls without parentheses
        with pytest.raises(ValueError, match=re.escape("fonksiyonundan sonra '(' gerekir")):
            evaluate_expression("sqrt 25 sin pi")

    def test_edge_cases(self):
        """Test edge cases for strict syntax validation."""
        # Single number (should work)
        assert evaluate_expression("5") == 5.0
        
        # Single function call with parentheses (should work)
        assert evaluate_expression("sqrt(25)") == 5.0
        
        # Single constant (should work)
        assert evaluate_expression("pi") == pytest.approx(3.14159)
        
        # Empty expression (should raise empty expression error, not syntax error)
        with pytest.raises(ValueError, match="Boş ifade"):
            evaluate_expression("")

    def test_existing_error_messages_unchanged(self):
        """Test that existing error messages remain unchanged."""
        # Unmatched parentheses
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression("(5 + 3")
        
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression("5 + 3)")
        
        with pytest.raises(ValueError, match="Eşleşmeyen parantez"):
            evaluate_expression(")5 + 3(")
        
        # Invalid characters
        with pytest.raises(ValueError, match="Geçersiz karakter"):
            evaluate_expression("5 % 3")
        
        # Invalid numbers
        with pytest.raises(ValueError, match="Geçersiz sayı formatı"):
            evaluate_expression("5.2.3 + 1")
        
        # Division by zero
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            evaluate_expression("5 / 0")
        
        # Square root of negative
        with pytest.raises(ValueError, match="Karekök negatif"):
            evaluate_expression("sqrt(-1)")
        
        # Log of zero or negative
        with pytest.raises(ValueError, match="Logaritma"):
            evaluate_expression("log(0)")
        
        with pytest.raises(ValueError, match="Doğal logaritma"):
            evaluate_expression("ln(0)")
