import random
import pyperclip


class Interface:
    def __init__(self):
        self.RED = "\033[91m"
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.BLUE = "\033[94m"
        self.MAGENTA = "\033[95m"
        self.RESET = "\033[0m"

    def display_hello_message(self):
        print(f"{self.GREEN}PassGenCLI - Password Generator Command Line Tool{self.RESET}")

    def display_menu(self):
        print(f"""1. Generate new password
2. Get saved password by it's context
3. Replace an alphabet character with a set of custom characters
4. Reset an alphabet character replacement to it's default
5. Clear history
0. Exit
        """)
        while True:
            try:
                choice = int(input("Select an option: "))
                if choice in [0, 1, 2, 3, 4, 5]:
                    return choice
                else:
                    print(f"{self.YELLOW}Invalid choice. Please select from 0 to 5.{self.RESET}")
            except ValueError:
                print(f"{self.RED}Invalid input. Please enter a number.{self.RESET}")

    def display_result(self, text, key, password):
        print(f"The Text is:              {text}")
        print(f"The Key is:               {key}")
        print(f"The Ciphered Text is:     {self.MAGENTA}{password}{self.RESET}")

    def display_error(self, context):
        print(f"{self.RED}There is no password saved with this context '{context}'{self.RESET}")

    def display_exit_message(self):
        print(f"{self.GREEN}Thanks for using it{self.RESET}")

    def get_text(self):
        text = str(input("Enter plain text: "))
        return text

    def get_key(self):
        key = str(input("Enter the key (or press Enter to skip): "))
        return key if key else ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(4, 6)))

    def get_context_to_save(self):
        context = str(input("Enter the context if you want to save the password in history (or press Enter to skip): "))
        return context if context else None

    def replace_character(self):
        return str(input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))

    def get_context_to_load(self):
        return str(input("Enter the context of the saved password: "))

    def reset_character(self):
        return str(input("Enter the character you want to reset it ot it's default: "))[0]

    def copy_to_clipboard(self, password):
        try:
            pyperclip.copy(password)
            print(f"{self.BLUE}Your password has been copied to your clipboard. Just paste it{self.RESET}")
        except pyperclip.PyperclipException:
            print(f"{self.RED}Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip){self.RESET}")
