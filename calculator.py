"""Simple calculator implementation."""

import math
from dataclasses import dataclass


@dataclass
class Token:
    """Represents a token in the expression."""
    type: str
    value: str | float


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


def tokenize(expr: str) -> list[Token]:
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
            tokens.append(Token('OPERATOR', '**'))
            i += 2
        elif ch in '+-*/()':
            # Handle unary minus (negative numbers)
            # Unary minus occurs after: start of expression, an operator, opening parenthesis, or another unary minus
            if ch == '-' and (i == 0 or not tokens or tokens[-1].type in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']):
                # This is a unary minus
                tokens.append(Token('UNARY_MINUS', ch))
                i += 1
            else:
                if ch == '(':
                    tokens.append(Token('LPAREN', ch))
                elif ch == ')':
                    tokens.append(Token('RPAREN', ch))
                else:
                    tokens.append(Token('OPERATOR', ch))
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
            tokens.append(Token('NUMBER', parse_number(num_str)))
            i = j
        elif ch.isalpha():
            # Functions and constants
            j = i
            while j < len(expr) and expr[j].isalpha():
                j += 1
            word = expr[i:j].lower()
            if word in ('sqrt', 'sin', 'cos', 'tan', 'log', 'ln'):
                tokens.append(Token('FUNCTION', word))
            elif word in ('pi', 'e'):
                tokens.append(Token('CONSTANT', word))
            else:
                raise ValueError(f"Bilinmeyen fonksiyon veya sabit: '{word}'")
            i = j
        else:
            raise ValueError(f"Geçersiz karakter: '{ch}'")
    
    return tokens


def _validate_tokens(tokens: list[Token]) -> None:
    """Validate token sequence to ensure proper alternation between operands and operators.
    
    Functions must be called with parentheses (e.g., sqrt(25) not sqrt 25).
    Operands and operators must alternate properly.
    """
    # A function name must be immediately followed by '('.
    for i, token in enumerate(tokens):
        if token.type == 'FUNCTION' and (i + 1 >= len(tokens) or tokens[i + 1].type != 'LPAREN'):
            raise ValueError(f"'{token.value}' fonksiyonundan sonra '(' gerekir")

    # Check parenthesis balance up front, so a stray ')' (e.g. ")5 + 3(")
    # reports the parenthesis error instead of a generic invalid-expression one.
    depth = 0
    for token in tokens:
        if token.type == 'LPAREN':
            depth += 1
        elif token.type == 'RPAREN':
            depth -= 1
            if depth < 0:
                raise ValueError("Eşleşmeyen parantez")
    if depth != 0:
        raise ValueError("Eşleşmeyen parantez")

    # Check that operands and operators alternate properly
    for i in range(len(tokens)):
        token = tokens[i]
        
        if i == 0:
            # First token can be: NUMBER, CONSTANT, UNARY_MINUS, LPAREN, FUNCTION
            if token.type not in ['NUMBER', 'CONSTANT', 'UNARY_MINUS', 'LPAREN', 'FUNCTION']:
                raise ValueError("Geçersiz ifade")
        else:
            prev_token = tokens[i-1]
            
            # Current token can be: NUMBER, CONSTANT, UNARY_MINUS, LPAREN, FUNCTION, OPERATOR, RPAREN
            if token.type == 'NUMBER':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_token.type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'CONSTANT':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_token.type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'UNARY_MINUS':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS, or start
                if prev_token.type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS'] and i > 0:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'LPAREN':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS, FUNCTION
                if prev_token.type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS', 'FUNCTION']:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'FUNCTION':
                # Previous must be: OPERATOR, LPAREN, UNARY_MINUS
                if prev_token.type not in ['OPERATOR', 'LPAREN', 'UNARY_MINUS']:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'OPERATOR':
                # Previous must be: NUMBER, CONSTANT, RPAREN
                if prev_token.type not in ['NUMBER', 'CONSTANT', 'RPAREN']:
                    raise ValueError("Geçersiz ifade")
            elif token.type == 'RPAREN':
                # Previous must be: NUMBER, CONSTANT, RPAREN
                if prev_token.type not in ['NUMBER', 'CONSTANT', 'RPAREN']:
                    raise ValueError("Geçersiz ifade")


# Operator and function dispatch dictionaries
OPERATORS = {
    '+': lambda a, b: _checked(Calculator().add(a, b)),
    '-': lambda a, b: _checked(Calculator().subtract(a, b)),
    '*': lambda a, b: _checked(Calculator().multiply(a, b)),
    '/': lambda a, b: _checked(Calculator().divide(a, b)),
    '**': lambda a, b: _check_power(a, b)
}

FUNCTIONS = {
    'sqrt': lambda a: math.sqrt(a) if a >= 0 else _raise_sqrt_negative(),
    'sin': lambda a: math.sin(a),
    'cos': lambda a: math.cos(a),
    'tan': lambda a: math.tan(a),
    'log': lambda a: math.log10(a) if a > 0 else _raise_log_negative(),
    'ln': lambda a: math.log(a) if a > 0 else _raise_ln_negative()
}


def _raise_sqrt_negative():
    raise ValueError("Karekök negatif sayı için tanımsızdır")


def _raise_log_negative():
    raise ValueError("Logaritma sıfır veya negatif için tanımsızdır")


def _raise_ln_negative():
    raise ValueError("Doğal logaritma sıfır veya negatif için tanımsızdır")


def to_rpn(tokens: list[Token]) -> list:
    """Convert tokens to Reverse Polish Notation using Shunting Yard algorithm."""
    output = []
    operators = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3, '**': 4}  # ** has highest precedence
    
    for token in tokens:
        if token.type == 'NUMBER':
            output.append(token.value)
        elif token.type == 'CONSTANT':
            if token.value == 'pi':
                output.append(math.pi)
            elif token.value == 'e':
                output.append(math.e)
        elif token.type == 'UNARY_MINUS':
            # Unary minus has lower precedence than ** (standard math convention)
            operators.append('u-')  # Use 'u-' to distinguish from binary '-'
        elif token.type == 'LPAREN':
            operators.append(token.value)
        elif token.type == 'RPAREN':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Eşleşmeyen parantez")
            operators.pop()  # Remove '('
            # If there's a function on the stack, apply it
            if operators and operators[-1] in FUNCTIONS:
                output.append(operators.pop())
        elif token.type == 'FUNCTION':
            operators.append(token.value)
        elif token.type == 'OPERATOR':
            # '**' is right-associative: pop only strictly higher precedence.
            # Other operators are left-associative: also pop equal precedence.
            while (operators and operators[-1] != '(' and
                   (precedence.get(operators[-1], 0) > precedence.get(token.value, 0) or
                    (token.value != '**' and
                     precedence.get(operators[-1], 0) == precedence.get(token.value, 0)))):
                output.append(operators.pop())
            operators.append(token.value)
    
    while operators:
        if operators[-1] in '()':
            raise ValueError("Eşleşmeyen parantez")
        output.append(operators.pop())
    
    return output


def eval_rpn(rpn: list) -> float:
    """Evaluate Reverse Polish Notation expression."""
    stack = []
    
    for token in rpn:
        if isinstance(token, float):
            stack.append(token)
        else:
            if token == 'u-':
                # Unary minus - only one operand needed
                if len(stack) < 1:
                    raise ValueError("Geçersiz ifade")
                a = stack.pop()
                stack.append(-a)
            elif token in FUNCTIONS:
                # Functions - one operand
                if len(stack) < 1:
                    raise ValueError("Geçersiz ifade")
                a = stack.pop()
                stack.append(FUNCTIONS[token](a))
            else:
                # Binary operators - need two operands
                if len(stack) < 2:
                    raise ValueError("Geçersiz ifade")
                b = stack.pop()
                a = stack.pop()
                stack.append(OPERATORS[token](a, b))
    
    if len(stack) != 1:
        raise ValueError("Geçersiz ifade")
    
    return stack[0]


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
    
    # Convert to RPN
    rpn = to_rpn(tokens)
    
    # Evaluate RPN
    return eval_rpn(rpn)


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
 
