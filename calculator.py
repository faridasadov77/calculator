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


def _checked(value: float) -> float:
    """Reject results that overflowed to inf (e.g. 10 ** 308 * 10) or became NaN."""
    if not math.isfinite(value):
        raise ValueError("Sonuç çok büyük (taşma)")
    return value


def _check_power(a: float, b: float) -> float:
    """Raise ValueError if a ** b would overflow, be complex, or divide by zero.
    
    Returns the validated result if successful.
    """
    try:
        result = a ** b
    except OverflowError:
        raise ValueError("Sonuç çok büyük (taşma)") from None
    except ZeroDivisionError:
        raise ValueError("Sıfır negatif bir üsse yükseltilemez") from None
    if isinstance(result, complex):
        raise ValueError("Negatif sayının kesirli üssü tanımsızdır")
    return result


def tokenize(expr: str) -> list:
    """Convert expression string into tokens (numbers, operators, parentheses, functions)."""
    tokens = []
    i = 0
    expr = expr.strip()
    
    while i < len(expr):
        ch = expr[i]
        
        if ch.isspace():
            i += 1
            continue
        
        if ch == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
            # Exponentiation operator ** (must be checked before single-char operators)
            tokens.append(('OPERATOR', '**'))
            i += 2
        elif ch in '+-*/()':
            # Handle unary minus (negative numbers)
            # Unary minus occurs after: start of expression, an operator, opening parenthesis, or another unary minus
            if ch == '-' and (i == 0 or not tokens or tokens[-1][0] in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']):
                # This is a unary minus
                tokens.append(('UNARY_MINUS', ch))
                i += 1
            else:
                if ch == '(':
                    tokens.append(('LPAREN', ch))
                elif ch == ')':
                    tokens.append(('RPAREN', ch))
                else:
                    tokens.append(('OPERATOR', ch))
                i += 1
        elif ch.isdigit() or ch == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            # Optional exponent (1e5, 2.5E-3). Only consumed when digits follow,
            # so "2 * e" and "2e" keep treating 'e' as Euler's constant.
            if j < len(expr) and expr[j] in 'eE':
                k = j + 1
                if k < len(expr) and expr[k] in '+-':
                    k += 1
                if k < len(expr) and expr[k].isdigit():
                    while k < len(expr) and expr[k].isdigit():
                        k += 1
                    j = k
            num_str = expr[i:j]
            tokens.append(('NUMBER', parse_number(num_str)))
            i = j
        elif ch.isalpha():
            # Functions and constants
            j = i
            while j < len(expr) and expr[j].isalpha():
                j += 1
            word = expr[i:j].lower()
            if word in ('sqrt', 'sin', 'cos', 'tan', 'log', 'ln'):
                tokens.append(('FUNCTION', word))
            elif word in ('pi', 'e'):
                tokens.append(('CONSTANT', word))
            else:
                raise ValueError(f"Bilinmeyen fonksiyon veya sabit: '{word}'")
            i = j
        else:
            raise ValueError(f"Geçersiz karakter: '{ch}'")
    
    return tokens


def _validate_tokens(tokens: list) -> None:
    """Validate token sequence to ensure proper alternation between operands and operators.
    
    Functions must be called with parentheses (e.g., sqrt(25) not sqrt 25).
    Operands and operators must alternate properly.
    """
    # A function name must be immediately followed by '('.
    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == 'FUNCTION' and (i + 1 >= len(tokens) or tokens[i + 1][0] != 'LPAREN'):
            raise ValueError(f"'{token_value}' fonksiyonundan sonra '(' gerekir")

    # Check parenthesis balance up front, so a stray ')' (e.g. ")5 + 3(")
    # reports the parenthesis error instead of a generic invalid-expression one.
    depth = 0
    for token_type, _ in tokens:
        if token_type == 'LPAREN':
            depth += 1
        elif token_type == 'RPAREN':
            depth -= 1
            if depth < 0:
                raise ValueError("Eşleşmeyen parantez")
    if depth != 0:
        raise ValueError("Eşleşmeyen parantez")

    # Check that operands and operators alternate properly
    for i in range(len(tokens)):
        token_type, token_value = tokens[i]
        
        if i == 0:
            # First token can be: NUMBER, CONSTANT, UNARY_MINUS, LPAREN, FUNCTION
            if token_type not in ['NUMBER', 'CONSTANT', 'UNARY_MINUS', 'LPAREN', 'FUNCTION']:
                raise ValueError("Geçersiz ifade")
        else:
            prev_type, prev_value = tokens[i-1]
            
            # Current token can be: NUMBER, CONSTANT, UNARY_MINUS, LPAREN, FUNCTION, OPERATOR, RPAREN
            if token_type == 'NUMBER':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'CONSTANT':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'UNARY_MINUS':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS, or start
                if prev_type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS'] and i > 0:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'LPAREN':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS, FUNCTION
                if prev_type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS', 'FUNCTION']:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'FUNCTION':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'OPERATOR':
                # Previous must be: NUMBER, CONSTANT, RPAREN
                if prev_type not in ['NUMBER', 'CONSTANT', 'RPAREN']:
                    raise ValueError("Geçersiz ifade")
            elif token_type == 'RPAREN':
                # Previous must be: NUMBER, CONSTANT, RPAREN
                if prev_type not in ['NUMBER', 'CONSTANT', 'RPAREN']:
                    raise ValueError("Geçersiz ifade")


def evaluate_expression(expr: str) -> float:
    """Evaluate a full mathematical expression with operator precedence.
    
    Supports:
    - Basic operations: +, -, *, /
    - Operator precedence: * and / before + and -
    - Left-to-right associativity
    - Parentheses for grouping
    - Negative numbers
    - Decimals
    - Flexible spacing
    - Exponentiation with ** (right-associative)
    - Functions: sqrt, sin, cos, tan, log (base 10), ln.
      They must be called with parentheses (e.g., sqrt(25)).
    - Constants: pi, e
    - Scientific notation: 1e5, 2.5E-3
    - Exponentiation binds tighter than unary minus, so -2 ** 2 == -4 (like Python)
    """
    if not expr or not expr.strip():
        raise ValueError("Boş ifade girilemez.")
    
    tokens = tokenize(expr)
    
    # Validate token sequence for strict syntax
    _validate_tokens(tokens)
    
    # Shunting Yard algorithm to convert to RPN
    output = []
    operators = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3, 'u+': 3, '**': 4}  # ** has highest precedence
    
    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            output.append(token_value)
        elif token_type == 'CONSTANT':
            if token_value == 'pi':
                output.append(math.pi)
            elif token_value == 'e':
                output.append(math.e)
        elif token_type == 'UNARY_MINUS':
            # Unary minus has lower precedence than ** (standard math convention)
            operators.append('u-')  # Use 'u-' to distinguish from binary '-'
        elif token_type == 'LPAREN':
            operators.append(token_value)
        elif token_type == 'RPAREN':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Eşleşmeyen parantez")
            operators.pop()  # Remove '('
            # If there's a function on the stack, apply it
            if operators and operators[-1] in ('sqrt', 'sin', 'cos', 'tan', 'log', 'ln'):
                output.append(operators.pop())
        elif token_type == 'FUNCTION':
            operators.append(token_value)
        elif token_type == 'OPERATOR':
            # '**' is right-associative: pop only strictly higher precedence.
            # Other operators are left-associative: also pop equal precedence.
            while (operators and operators[-1] != '(' and
                   (precedence.get(operators[-1], 0) > precedence.get(token_value, 0) or
                    (token_value != '**' and
                     precedence.get(operators[-1], 0) == precedence.get(token_value, 0)))):
                output.append(operators.pop())
            operators.append(token_value)
    
    while operators:
        if operators[-1] in '()':
            raise ValueError("Eşleşmeyen parantez")
        output.append(operators.pop())
    
    # Evaluate RPN
    stack = []
    calc = Calculator()
    
    for token in output:
        if isinstance(token, float):
            stack.append(token)
        else:
            if token == 'u-':
                # Unary minus - only one operand needed
                if len(stack) < 1:
                    raise ValueError("Geçersiz ifade")
                a = stack.pop()
                stack.append(-a)
            elif token in ('sqrt', 'sin', 'cos', 'tan', 'log', 'ln'):
                # Functions - one operand
                if len(stack) < 1:
                    raise ValueError("Geçersiz ifade")
                a = stack.pop()
                if token == 'sqrt':
                    if a < 0:
                        raise ValueError("Karekök negatif sayı için tanımsızdır")
                    stack.append(math.sqrt(a))
                elif token == 'sin':
                    stack.append(math.sin(a))
                elif token == 'cos':
                    stack.append(math.cos(a))
                elif token == 'tan':
                    stack.append(math.tan(a))
                elif token == 'log':
                    if a <= 0:
                        raise ValueError("Logaritma sıfır veya negatif için tanımsızdır")
                    stack.append(math.log10(a))
                elif token == 'ln':
                    if a <= 0:
                        raise ValueError("Doğal logaritma sıfır veya negatif için tanımsızdır")
                    stack.append(math.log(a))
            else:
                # Binary operators - need two operands
                if len(stack) < 2:
                    raise ValueError("Geçersiz ifade")
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(_checked(calc.add(a, b)))
                elif token == '-':
                    stack.append(_checked(calc.subtract(a, b)))
                elif token == '*':
                    stack.append(_checked(calc.multiply(a, b)))
                elif token == '/':
                    stack.append(_checked(calc.divide(a, b)))
                elif token == '**':
                    stack.append(_check_power(a, b))
    
    if len(stack) != 1:
        raise ValueError("Geçersiz ifade")
    
    return stack[0]


def parse_expression(expr: str) -> tuple[float, str, float]:
    """Parse and validate a simple binary expression (for backward compatibility).
    
    This maintains the old API for tests that expect a tuple return.
    For full expression evaluation, use evaluate_expression().

    Note: the tuple splits at the first top-level operator, so ``a op b`` does
    not always equal the full result (e.g. "10 - 5 - 2" gives (10.0, '-', 3.0)).
    """
    # Try to evaluate as full expression first
    result = evaluate_expression(expr)
    
    # For backward compatibility, we still need to return a tuple
    # This is a simplified parse - just find the first top-level operator
    tokens = tokenize(expr)
    
    # Find first operator at depth 0 (not inside parentheses)
    depth = 0
    for i, (token_type, token_value) in enumerate(tokens):
        if token_type == 'LPAREN':
            depth += 1
        elif token_type == 'RPAREN':
            depth -= 1
        elif token_type == 'OPERATOR' and depth == 0 and token_value in '+-*/':
            # Found top-level operator
            left_tokens = tokens[:i]
            right_tokens = tokens[i+1:]
            
            # Evaluate left and right sides
            left_expr = ' '.join(str(v) if t == 'NUMBER' else v for t, v in left_tokens)
            right_expr = ' '.join(str(v) if t == 'NUMBER' else v for t, v in right_tokens)
            
            a = evaluate_expression(left_expr) if left_expr else 0
            b = evaluate_expression(right_expr) if right_expr else 0
            
            return a, token_value, b
    
    # Fallback: single number
    return result, '+', 0


def main():
    print("Hesap Makinesi")
    print("İşlemler: +, -, *, /, ** (üs alma)")
    print("Fonksiyonlar: sqrt, sin, cos, tan, log, ln")
    print("Sabitler: pi, e")
    print("Parantez desteklenir: (5 + 3) * 2")
    print("Örnekler: 5 + 3 * 2, (5 + 3) * 2, sqrt(25), 2 ** 3, sin(pi/2)")
    print("Çıkmak için 'q' yazın")

    while True:
        try:
            expr = input("\nİşlem girin (örn: 5 + 3): ")
            if expr.strip().lower() == 'q':
                break

            result = evaluate_expression(expr)
            print(f"Sonuç: {result}")

        except (ValueError, ArithmeticError) as e:
            print(f"Hata: {e}")
        except KeyboardInterrupt:
            print("\nÇıkılıyor...")
            break
        except EOFError:
            break

    print("Güle güle!")


if __name__ == "__main__":
    main()