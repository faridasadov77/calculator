"""Simple calculator implementation."""

import math


class Calculator:
    """Basic calculator supporting four operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def parse_number(s: str) -> float:
    """Parse a string to float with validation."""
    s = s.strip()
    if not s:
        raise ValueError("Boş sayı girişi")
    
    try:
        value = float(s)
    except ValueError:
        raise ValueError(f"Geçersiz sayı formatı: '{s}'")
    
    if math.isnan(value):
        raise ValueError("NaN (Not a Number) geçersizdir")
    if math.isinf(value):
        raise ValueError("Sonsuz değer geçersizdir")
    
    return value


def validate_operator(op: str) -> str:
    """Validate and return operator."""
    valid_ops = {'+', '-', '*', '/'}
    if op not in valid_ops:
        raise ValueError(f"Geçersiz operatör: '{op}'. Kullan: +, -, *, /")
    return op


def parse_expression(expr: str) -> tuple[float, str, float]:
    """Parse and validate a full expression string.
    
    Supports flexible formats:
    - "5 + 3" (space-separated)
    - "5+3" (no spaces)
    - "5 +3" / "5+ 3" (partial spaces)
    - "-5 + 3" (negative numbers)
    - "5.5 * -2.3" (decimals with negatives)
    """
    if not expr or not expr.strip():
        raise ValueError("Boş ifade girilemez.")
    
    expr = expr.strip()
    
    # Find operator position (skip leading sign of first number)
    operators = ['+', '-', '*', '/']
    op_pos = -1
    op_char = ''
    
    for i, ch in enumerate(expr):
        if ch in operators:
            # Skip if it's the first character (negative sign for first number)
            if i == 0:
                continue
            # Skip if previous char is an operator (e.g., "5*-3" -> '*' at pos 1, '-' at pos 2)
            if expr[i-1] in operators:
                continue
            op_pos = i
            op_char = ch
            break
    
    if op_pos == -1:
        raise ValueError("Geçersiz format. Operatör bulunamadı (+, -, *, /).")
    
    left_str = expr[:op_pos].strip()
    right_str = expr[op_pos+1:].strip()
    
    if not left_str or not right_str:
        raise ValueError("Geçersiz format. Her iki tarafında da sayı olmalı.")
    
    a = parse_number(left_str)
    op = validate_operator(op_char)
    b = parse_number(right_str)
    
    return a, op, b


def main():
    calc = Calculator()
    print("Hesap Makinesi")
    print("İşlemler: +, -, *, /")
    print("Çıkmak için 'q' yazın")

    while True:
        try:
            expr = input("\nİşlem girin (örn: 5 + 3): ")
            if expr.strip().lower() == 'q':
                break

            a, op, b = parse_expression(expr)

            if op == '+':
                result = calc.add(a, b)
            elif op == '-':
                result = calc.subtract(a, b)
            elif op == '*':
                result = calc.multiply(a, b)
            elif op == '/':
                result = calc.divide(a, b)

            print(f"Sonuç: {result}")

        except ValueError as e:
            print(f"Hata: {e}")
        except KeyboardInterrupt:
            print("\nÇıkılıyor...")
            break
        except EOFError:
            break

    print("Güle güle!")


if __name__ == "__main__":
    main()