"""Simple calculator implementation."""


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


def main():
    calc = Calculator()
    print("Hesap Makinesi")
    print("İşlemler: +, -, *, /")
    print("Çıkmak için 'q' yazın")

    while True:
        try:
            expr = input("\nİşlem girin (örn: 5 + 3): ").strip()
            if expr.lower() == 'q':
                break

            parts = expr.split()
            if len(parts) != 3:
                print("Format: sayı operatör sayı (örn: 5 + 3)")
                continue

            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])

            if op == '+':
                result = calc.add(a, b)
            elif op == '-':
                result = calc.subtract(a, b)
            elif op == '*':
                result = calc.multiply(a, b)
            elif op == '/':
                result = calc.divide(a, b)
            else:
                print("Geçersiz operatör. Kullan: +, -, *, /")
                continue

            print(f"Sonuç: {result}")

        except ValueError as e:
            print(f"Hata: {e}")
        except KeyboardInterrupt:
            break

    print("Güle güle!")


if __name__ == "__main__":
    main()