#!/usr/bin/env python3
"""Simple test to verify the patch works correctly."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from calculator import evaluate_expression

def test_patch():
    """Test that the patch changes work correctly."""
    
    print("Testing patch changes...")
    
    # Test 1: Functions without parentheses should be rejected
    try:
        evaluate_expression("sqrt 25")
        print("❌ FAIL: sqrt 25 should be rejected")
        return False
    except ValueError as e:
        if "fonksiyonundan sonra '(' gerekir" in str(e):
            print("✅ PASS: sqrt 25 correctly rejected")
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            return False
    
    # Test 2: Functions with parentheses should work
    try:
        result = evaluate_expression("sqrt(25)")
        if result == 5.0:
            print("✅ PASS: sqrt(25) works correctly")
        else:
            print(f"❌ FAIL: sqrt(25) returned {result}, expected 5.0")
            return False
    except Exception as e:
        print(f"❌ FAIL: sqrt(25) failed: {e}")
        return False
    
    # Test 3: Unmatched parentheses should report "Eşleşmeyen parantez"
    try:
        evaluate_expression(")5 + 3(")
        print("❌ FAIL: )5 + 3( should be rejected")
        return False
    except ValueError as e:
        if "Eşleşmeyen parantez" in str(e):
            print("✅ PASS: )5 + 3( correctly rejected with parenthesis error")
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            return False
    
    # Test 4: Bare function name at end should be rejected
    try:
        evaluate_expression("2 * sin")
        print("❌ FAIL: 2 * sin should be rejected")
        return False
    except ValueError as e:
        if "fonksiyonundan sonra '(' gerekir" in str(e):
            print("✅ PASS: 2 * sin correctly rejected")
        else:
            print(f"❌ FAIL: Wrong error message: {e}")
            return False
    
    # Test 5: Valid expressions should still work
    try:
        result = evaluate_expression("5 + 3 * 2")
        if result == 11.0:
            print("✅ PASS: 5 + 3 * 2 works correctly")
        else:
            print(f"❌ FAIL: 5 + 3 * 2 returned {result}, expected 11.0")
            return False
    except Exception as e:
        print(f"❌ FAIL: 5 + 3 * 2 failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Patch is working correctly.")
    return True

if __name__ == "__main__":
    success = test_patch()
    sys.exit(0 if success else 1)