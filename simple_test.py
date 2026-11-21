#!/usr/bin/env python3
"""Simple test to verify unary minus fix"""

import sys
sys.path.append('.')

from calculator import evaluate_expression

# Test the specific cases mentioned in the bug report
test_cases = [
    ("5 * -2", -10),      # Should work (no space)
    ("5 + -3", 2),        # Should work (no space)  
    ("3 - -2", 5),        # Should work (no space)
    ("5+-3", 2),          # Should work (no space)
    ("3--2", 5),          # Should work (no space)
    ("-(3+2)", -5),       # Should work after fix
    ("- 5", -5),          # Should work after fix
    ("5 * - 2", -10),     # Should work after fix (space before minus)
    ("5 + - 3", 2),       # Should work after fix (space before minus)
    ("3 - - 2", 5),       # Should work after fix (space before minus)
]

print("Testing unary minus cases:")
print("=" * 50)

all_passed = True

for i, (expr, expected) in enumerate(test_cases, 1):
    try:
        result = evaluate_expression(expr)
        if result == expected:
            print(f"{i:2d}. '{expr}' -> {result} ✓")
        else:
            print(f"{i:2d}. '{expr}' -> {result} (expected {expected}) ✗")
            all_passed = False
    except Exception as e:
        print(f"{i:2d}. '{expr}' -> ERROR: {e} ✗")
        all_passed = False

print("=" * 50)
if all_passed:
    print("All tests passed! ✓")
else:
    print("Some tests failed! ✗")