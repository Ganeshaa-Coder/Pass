import random
import string
import csv

def generate_password(length, use_upper=True, use_digits=True, use_symbols=True):
    characters = list(string.ascii_lowercase)
    if use_upper:
        characters += list(string.ascii_uppercase)
    if use_digits:
        characters += list(string.digits)
    if use_symbols:
        characters += list("!@#$%^&*()-_=+[]{}|;:,.<>?")

    if not characters:
        # Return a specific indicator instead of just a string
        # This allows the caller (main) to handle it more robustly
        return None # Indicate failure due to no character types

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("🔐 Multiple Password Generator")
    print("-" * 30) # Separator for visual clarity

    # --- Get Password Criteria ---
    while True: # Loop for valid length input
        try:
            length_input = input("Enter desired password length (e.g., 12): ")
            length = int(length_input)
            if length <= 0:
                print("   Error: Please enter a positive number for length.")
            else:
                break # Exit loop if input is a valid positive integer
        except ValueError:
            print("   Error: Invalid input. Please enter a whole number.")

    use_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

    # Check if at least one character set is selected
    if not string.ascii_lowercase and not use_upper and not use_digits and not use_symbols:
         # This check is technically redundant if generate_password handles it,
         # but good for early feedback. The list(string.ascii_lowercase) always adds lowercase.
         # Let's refine generate_password to handle the case where NO options are selected
         # even if lowercase is default. (Though current logic forces lowercase)
         # We'll rely on generate_password returning None if no chars are available.
         pass # Let generate_password handle this

    # --- Get Number of Passwords ---
    while True: # Loop for valid number of passwords input
        try:
            num_passwords_input = input("How many passwords do you want to generate? ")
            num_passwords = int(num_passwords_input)
            if num_passwords <= 0:
                print("   Error: Please enter a positive number.")
            else:
                break # Exit loop if input is valid
        except ValueError:
            print("   Error: Invalid input. Please enter a whole number.")

    # --- Generate Passwords ---
    passwords = []
    print("\nGenerating passwords...")
    for i in range(num_passwords):
        password = generate_password(length, use_upper, use_digits, use_symbols)
        if password is None: # Check if generate_password indicated failure
             print("\nError: No character types selected (lowercase, uppercase, digits, symbols). Cannot generate passwords.")
             print("Exiting.")
             return # Exit main function early

        passwords.append(password)
        # Optional: Add progress indicator for large numbers
        # if num_passwords > 10 and (i + 1) % (num_passwords // 10) == 0:
        #    print(f"  Generated {i + 1}/{num_passwords}...")

    # --- Display Passwords ---
    print("\nGenerated passwords:")
    print("-" * 20)
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}: {pwd}")
    print("-" * 20)

    # --- Save to CSV Option ---
    while True: # Loop for valid save choice input
        save_choice = input("\nSave passwords to a CSV file? (y/n): ").strip().lower()
        if save_choice in ['y', 'n']:
            break
        else:
            print("   Error: Invalid input. Please enter 'y' or 'n'.")

    if save_choice == 'y':
        while True: # Loop for valid filename
            filename_base = input("Enter filename (e.g., 'my_passwords', without .csv extension): ").strip()
            if not filename_base:
                print("   Error: Filename cannot be empty.")
                continue

            # Basic check for potentially problematic characters in filenames
            invalid_chars = r'<>:"/\|?*'
            if any(c in invalid_chars for c in filename_base):
                 print(f"   Error: Filename contains invalid characters ({invalid_chars}). Please use a different name.")
                 continue

            # Check for reserved filenames on Windows (optional, but good practice)
            # reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", ...]
            # if filename_base.upper() in reserved_names:
            #     print("   Error: Filename is reserved. Please choose another.")
            #     continue

            filename_csv = f"{filename_base}.csv"
            break # Exit loop if filename seems okay

        try:
            with open(filename_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Optional: Add a header row
                # writer.writerow(["Password"])
                for pwd in passwords:
                    writer.writerow([pwd]) # Write password in its own row
            print(f"\nPasswords successfully saved to '{filename_csv}'")
        except IOError as e:
            # Provide more specific feedback if possible
            print(f"\nError: Could not write to file '{filename_csv}'.")
            print(f"   Reason: {e}") # Display the OS error message
        except Exception as e: # Catch other potential errors during file op
             print(f"\nAn unexpected error occurred while saving the file: {e}")

    # --- Final Message ---
    print("\nPassword generation process complete. Goodbye!")

if __name__ == "__main__":
    main()
