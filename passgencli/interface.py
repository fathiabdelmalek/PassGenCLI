import random
import pyperclip


class Interface:
    def display_menu(self):
        print("""
PassGenCLI - Password Generator Command Line Tool

1. Generate new password
2. Replace an alphabet character with a set of custom characters
3. Reset an alphabet character replacement to it's default
4. Clear history
0. Exit
        """)
        while True:
            try:
                choice = int(input("Select an option: "))
                if choice in [0, 1, 2, 3]:
                    return choice
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_text(self):
        text = str(input("Enter plain text: "))
        return text

    def get_key(self):
        key = str(input("Enter the key (or press Enter to skip): "))
        return key if key else ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(4, 6)))

    def replace_character(self):
        return str(input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))

    def reset_character(self):
        return str(input("Enter the character you want to reset it ot it's default: "))[0]

    def display_result(self, text, key, password):
        print(f"The Text is:              {text}")
        print(f"The Key is:               {key}")
        print(f"The Ciphered Text is:     {password}")

    def copy_to_clipboard(self, password):
        try:
            pyperclip.copy(password)
            print("Your password has been copied to your clipboard. Just paste it")
        except pyperclip.PyperclipException:
            print("Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip)")
