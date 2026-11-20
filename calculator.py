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
    """Parse and validate expression string."""
    expr = expr.strip()
    if not expr:
        raise ValueError("Boş ifade")
    
    parts = expr.split()
    if len(parts) != 3:
        raise ValueError("Format: sayı operatör sayı (örn: 5 + 3)")
    
    a = parse_number(parts[0])
    op = validate_operator(parts[1])
    b = parse_number(parts[2])
    
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