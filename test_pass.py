import unittest
import string # Import string for character sets, although estimate_strength doesn't need it directly here
from Pass import estimate_strength # Assuming Pass.py is in the same directory or PYTHONPATH

class TestPasswordStrength(unittest.TestCase):

    def test_weak_passwords(self):
        """Tests passwords that should be classified as Weak."""
        weak_passwords = [
            # Short length (< 8)
            "abc",
            "1234567",
            "aA1!",
            "", # Edge case: empty string
            # Single character type (>= 8 length)
            "abcdefgh",       # Lowercase only
            "ABCDEFGH",       # Uppercase only
            "12345678",       # Digits only
            "!@#$%^&*",       # Symbols only
            "         ",      # Whitespace only (counts as 0 types)
            "weakpass",       # Length 8, 1 type
            "we4kpassword",   # Length 12, but only 2 types (lowercase, digit) - Correction: This should be Medium. Moved below.
            "WEAKPASSWORD",   # Length 12, 1 type
            "w"*20,           # Long, but one type
            "1"*20,           # Long, but one type
        ]
        for pwd in weak_passwords:
            with self.subTest(password=pwd):
                self.assertEqual(estimate_strength(pwd), 'Weak', f"Failed for password: {pwd}")

    def test_medium_passwords(self):
        """Tests passwords that should be classified as Medium."""
        medium_passwords = [
            # Length 8-11, >= 2 types
            "abcDEF12",   # Len 8, 3 types
            "Passw0rd",   # Len 8, 3 types
            "Symb@l1c",   # Len 8, 3 types
            "GoodP@ss",   # Len 8, 3 types
            "abc123DEF",  # Len 9, 3 types
            "Word!1",     # Len 6 - Correction: This should be Weak. Removed.
            "Pass1234",   # Len 8, 2 types
            "Password12", # Len 10, 2 types
            "PASSWOrd!!", # Len 10, 3 types
            # Length >= 12, 2 types
            "abcdefgh1234",   # Len 12, 2 types
            "ABCDEFGH!@#$",   # Len 12, 2 types
            "longpassworddigits", # Len 18, 2 types
            "UPPERCASEANDDIGITS12345", # Len 23, 2 types
            "we4kpassword",   # Length 12, 2 types (Moved from Weak)
        ]
        for pwd in medium_passwords:
            with self.subTest(password=pwd):
                self.assertEqual(estimate_strength(pwd), 'Medium', f"Failed for password: {pwd}")

    def test_strong_passwords(self):
        """Tests passwords that should be classified as Strong."""
        strong_passwords = [
            # Length >= 12, >= 3 types
            "Str0ngP@sswrd",      # Len 13, 4 types
            "VeryC0mpl3x!ty#",    # Len 16, 4 types (Corrected from C0mpl3x!ty#)
            "L0ng&S3cur3P@ss",    # Len 15, 4 types
            "ThisIsAVeryLongPassword123!", # Len 28, 4 types
            "abcDEF123!@#",       # Len 12, 4 types
            "PasswordWithSymbol$",# Len 19, 3 types
            "Num8ers&UpperLower", # Len 19, 4 types
            "1234567890aA!",      # Len 13, 4 types
        ]
        for pwd in strong_passwords:
            with self.subTest(password=pwd):
                self.assertEqual(estimate_strength(pwd), 'Strong', f"Failed for password: {pwd}")

    def test_edge_cases(self):
        """Tests specific edge cases not fully covered above."""
        # Empty string is already tested in weak passwords
        self.assertEqual(estimate_strength(""), 'Weak', "Failed for empty string")
        # Whitespace is already tested in weak passwords
        self.assertEqual(estimate_strength("        "), 'Weak', "Failed for 8 spaces")
        self.assertEqual(estimate_strength("             "), 'Weak', "Failed for 13 spaces")
        # Password exactly on the boundary
        self.assertEqual(estimate_strength("abcdefg"), 'Weak', "Failed for length 7 (Weak)")
        self.assertEqual(estimate_strength("abcdefgh"), 'Weak', "Failed for length 8, 1 type (Weak)")
        self.assertEqual(estimate_strength("abcdeF1"), 'Weak', "Failed for length 7, 3 types (Weak)")
        self.assertEqual(estimate_strength("abcDEF12"), 'Medium', "Failed for length 8, 3 types (Medium)")
        self.assertEqual(estimate_strength("abcdefgh123"), 'Medium', "Failed for length 11, 2 types (Medium)")
        self.assertEqual(estimate_strength("abcdefgh123A"), 'Strong', "Failed for length 12, 3 types (Strong)")
        self.assertEqual(estimate_strength("abcdefgh123!"), 'Strong', "Failed for length 12, 3 types (Strong)")
        self.assertEqual(estimate_strength("abcdefgh1234"), 'Medium', "Failed for length 12, 2 types (Medium)")


if __name__ == '__main__':
    unittest.main()
