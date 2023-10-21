import random
import pyperclip


class Interface:
    def __init__(self):
        self._RED = "\033[91m"
        self._GREEN = "\033[92m"
        self._YELLOW = "\033[93m"
        self._BLUE = "\033[94m"
        self._MAGENTA = "\033[95m"
        self._DEFAULT = "\033[0m"

    @property
    def RED(self):
        return self._RED

    @property
    def GRENN(self):
        return self._GREEN

    @property
    def YELLOW(self):
        return self._YELLOW

    @property
    def BLUE(self):
        return self._BLUE

    @property
    def MAGENTA(self):
        return self._MAGENTA

    @property
    def DEFAULT(self):
        return self._DEFAULT

    def _display_menu(self, m, r):
        print(m)
        while True:
            try:
                choice = int(input("Select and option: "))
                if choice in r:
                    return choice
                print(f"{self._YELLOW}Invalid choice. Please select from 0 to {len(r)-1}.{self._DEFAULT}")
            except ValueError:
                print(f"{self._RED}Invalid input. Please enter a number.{self._DEFAULT}")

    def display_hello_message(self):
        print(f"{self._GREEN}PassGenCLI - Password Generator Command Line Tool{self._DEFAULT}")

    def display_main_menu(self):
        m = """1. Manage Passwords
2. Manage Configurations
3. Manage History
0. Exit"""
        r = [0, 1, 2, 3]
        return self._display_menu(m, r)

    def display_passwords_menu(self):
        m = """1.  Back
2.  Generate new password
3.  Update saved password on history
4.  Remove saved password from history
0.  Exit"""
        r = [0, 1, 2, 3, 4]
        return self._display_menu(m, r)

    def display_config_menu(self):
        m = """1.  Back
2.  Change the shift of the encryption
3.  Reset the shift to its default value
4.  Replace an alphabet character with a set of custom characters
5.  Reset an alphabet character replacement to it's default
6.  Show all characters replacements
7.  Change encryption method
8.  Reset default encryption method
9.  Encrypt history file
10.  Decrypt history file
11.  Show character replacement
12. Show all characters replacements
0.  Exit"""
        r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return self._display_menu(m, r)

    def display_history_menu(self):
        m = """1.  Back
2.  Retrieve saved password from history
3.  Show all saved passwords
4.  Clear history
5.  Back up history into backup file
6.  Load history from a back up from backup file
0.  Exit"""
        r = [0, 1, 2, 3, 4, 5, 6]
        return self._display_menu(m, r)

    def display_password(self, text, key, password, context=None):
        if context is not None:
            print(f"The context is:             {context}")
        print(f"The Text is:                {text}")
        print(f"The Key is:                 {key}")
        print(f"The Password is:            {self._MAGENTA}{password}{self._DEFAULT}")

    def display_character_replacement(self, character, replacement):
        print(f"{character} => {replacement}")

    def display_password_removed_message(self):
        print(f"{self.RED}This password was removed from memory, if you want to restore it, regenerate it.{self.DEFAULT}")

    def display_context_error_message(self, context):
        print(f"{self._RED}There is no password saved with this context '{context}'{self._DEFAULT}")

    def display_replacement_error_message(self, replacement):
        print(f"{self.RED}'{replacement}' is not a valid replacement, you should chose another replacement\n"
              f"Allowed special character: ('!', '@', '$', '^', '-', '_', '=', '+', '*', ',', '.', '/', ':'){self.DEFAULT}")

    def display_exit_message(self):
        print(f"{self._GREEN}Thanks for using it. Bye{self._DEFAULT}")

    def get_text(self):
        text = str(input("Enter plain text: "))
        return text

    def get_text_to_update(self):
        text = str(input("Enter plain text (or press Enter to skip): "))
        return text if text else None

    def get_key(self, none: bool = False):
        key = str(input("Enter the key (or press Enter to skip): "))
        return key if key else None if none else ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(4, 6)))

    def get_shift(self):
        shift = str(input("Enter the shift number (between 1 and 25 or press Enter for default value): "))
        return shift if shift in range(1, 26) else 5

    def get_context_to_save(self):
        context = str(input("Enter the context if you want to save the password in history (or press Enter to skip): "))
        return context if context else None

    def get_context_to_load(self):
        return str(input("Enter the context of the saved password: "))

    def get_character(self):
        return str(input("Which character ? "))

    def replace_character(self):
        return str(input("Enter the character you want to replace it: "))[0], str(input("Enter the replacement: "))

    def reset_character(self):
        return str(input("Enter the character you want to reset it ot it's default: "))[0]

    def copy_to_clipboard(self, password):
        try:
            pyperclip.copy(password)
            print(f"{self._BLUE}Your password has been copied to your clipboard. Just paste it{self._DEFAULT}")
        except pyperclip.PyperclipException:
            print(f"{self._RED}Your system doesn't have a copy/paste mechanism, try installing one (e.g., xclip){self._DEFAULT}")
