#!/usr/bin/env python3
"""Test script to verify unary minus functionality."""

import sys
sys.path.append('.')
from calculator import evaluate_expression

def test_unary_minus():
    """Test cases that should work with unary minus."""
    
    # These should work according to the current implementation
    test_cases_working = [
        ("5+-3", 2),
        ("3--2", 5),
        ("-5", -5),
        ("-2.5", -2.5),
        ("5*-2", -10),  # This might work if the minus is attached to 2
    ]
    
    # These should fail with current implementation
    test_cases_failing = [
        ("5 * -2", -10),  # Space before minus
        ("5 + -3", 2),    # Space before minus  
        ("3 - -2", 5),    # Space before minus
        ("-(3+2)", -5),   # Minus followed by parenthesis
        ("- 5", -5),      # Space after minus
    ]
    
    print("Testing cases that should work:")
    for expr, expected in test_cases_working:
        try:
            result = evaluate_expression(expr)
            print(f"  {expr} = {result} (expected {expected}) - {'✓' if result == expected else '✗'}")
        except Exception as e:
            print(f"  {expr} = ERROR: {e} - ✗")
    
    print("\nTesting cases that should fail:")
    for expr, expected in test_cases_failing:
        try:
            result = evaluate_expression(expr)
            print(f"  {expr} = {result} (expected {expected}) - {'✓' if result == expected else '✗'}")
        except Exception as e:
            print(f"  {expr} = ERROR: {e} - ✗")

if __name__ == "__main__":
    test_unary_minus()