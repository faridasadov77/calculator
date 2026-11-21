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


def tokenize(expr: str) -> list:
    """Convert expression string into tokens (numbers, operators, parentheses)."""
    tokens = []
    i = 0
    expr = expr.strip()
    
    while i < len(expr):
        ch = expr[i]
        
        if ch.isspace():
            i += 1
            continue
        
        if ch in '+-*/()':
            # Handle unary minus (negative numbers)
            # Unary minus occurs after: start of expression, an operator, or opening parenthesis
            if ch == '-' and (i == 0 or not tokens or tokens[-1][0] in ['OPERATOR', 'LPAREN']):
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
            num_str = expr[i:j]
            tokens.append(('NUMBER', parse_number(num_str)))
            i = j
        else:
            raise ValueError(f"Geçersiz karakter: '{ch}'")
    
    return tokens


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
    """
    if not expr or not expr.strip():
        raise ValueError("Boş ifade girilemez.")
    
    tokens = tokenize(expr)
    
    # Shunting Yard algorithm to convert to RPN
    output = []
    operators = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3}  # Unary minus has highest precedence
    
    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            output.append(token_value)
        elif token_type == 'UNARY_MINUS':
            # Unary minus has higher precedence than other operators
            operators.append('u-')  # Use 'u-' to distinguish from binary '-'
        elif token_type == 'LPAREN':
            operators.append(token_value)
        elif token_type == 'RPAREN':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Eşleşmeyen parantez")
            operators.pop()  # Remove '('
        elif token_type == 'OPERATOR':
            while (operators and operators[-1] != '(' and 
                   precedence.get(operators[-1], 0) >= precedence.get(token_value, 0)):
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
            else:
                # Binary operators - need two operands
                if len(stack) < 2:
                    raise ValueError("Geçersiz ifade")
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    stack.append(calc.add(a, b))
                elif token == '-':
                    stack.append(calc.subtract(a, b))
                elif token == '*':
                    stack.append(calc.multiply(a, b))
                elif token == '/':
                    stack.append(calc.divide(a, b))
    
    if len(stack) != 1:
        raise ValueError("Geçersiz ifade")
    
    return stack[0]


def parse_expression(expr: str) -> tuple[float, str, float]:
    """Parse and validate a simple binary expression (for backward compatibility).
    
    This maintains the old API for tests that expect a tuple return.
    For full expression evaluation, use evaluate_expression().
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
    print("İşlemler: +, -, *, /")
    print("Parantez desteklenir: (5 + 3) * 2")
    print("Çıkmak için 'q' yazın")

    while True:
        try:
            expr = input("\nİşlem girin (örn: 5 + 3): ")
            if expr.strip().lower() == 'q':
                break

            result = evaluate_expression(expr)
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