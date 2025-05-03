import random
import string

def generate_password(length, use_upper=True, use_digits=True, use_symbols=True):
    characters = list(string.ascii_lowercase)
    if use_upper:
        characters += list(string.ascii_uppercase)
    if use_digits:
        characters += list(string.digits)
    if use_symbols:
        characters += list("!@#$%^&*()-_=+[]{}|;:,.<>?")

    if not characters:
        return "No character types selected."

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def estimate_strength(password):
    """Estimates the strength of a password based on length and character variety."""
    length = len(password)
    types_count = 0
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    # Using the same symbol set as generate_password for consistency
    symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    has_symbol = any(c in symbols for c in password)

    if has_lower:
        types_count += 1
    if has_upper:
        types_count += 1
    if has_digit:
        types_count += 1
    if has_symbol:
        types_count += 1

    # Strength criteria evaluation
    if length < 8 or types_count <= 1:
        return 'Weak'
    # Note: Order matters. Check Strong condition before Medium.
    elif length >= 12 and types_count >= 3:
        return 'Strong'
    # Covers length 8-11 with >= 2 types AND length >= 12 with 2 types
    elif length >= 8 and types_count >= 2:
         return 'Medium'
    else:
        # Fallback case - should primarily be covered by the first condition.
        return 'Weak'

def main():
    print("🔐 Password Generator")
    length = int(input("Enter password length: "))
    use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    password = generate_password(length, use_upper, use_digits, use_symbols)
    print(f"Generated password: {password}")
    # Display estimated strength
    strength = estimate_strength(password)
    print(f"Estimated strength: {strength}")


if __name__ == "__main__":
    main()
