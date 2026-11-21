#!/usr/bin/env python3
"""Manual test runner for calculator tests"""

import sys
sys.path.append('.')

from calculator import evaluate_expression

# Test cases that should work according to the bug report
test_cases = [
    "5 * -2",      # Should work (no space)
    "5 + -3",      # Should work (no space)  
    "3 - -2",      # Should work (no space)
    "5+-3",        # Should work (no space)
    "3--2",        # Should work (no space)
    "-(3+2)",      # Should fail currently
    "- 5",         # Should fail currently
    "5 * - 2",     # Should fail currently (space before minus)
    "5 + - 3",     # Should fail currently (space before minus)
    "3 - - 2",     # Should fail currently (space before minus)
]

print("Testing unary minus cases:")
print("=" * 50)

for i, expr in enumerate(test_cases, 1):
    try:
        result = evaluate_expression(expr)
        print(f"{i:2d}. '{expr}' -> {result} ✓")
    except Exception as e:
        print(f"{i:2d}. '{expr}' -> ERROR: {e} ✗")