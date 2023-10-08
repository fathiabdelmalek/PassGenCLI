from passwords_generator import PasswordGenerator


class Generator:
    def __init__(self):
        self._generator = PasswordGenerator()
        
    def generate_password(self, text, key):
        self._generator.text = text
        self._generator.key = key
        return self._generator.generate_password()

    def replace_character(self, character, replacement):
        self._generator.replace_character(character, replacement)

    def reset_character(self, character):
        self._generator.reset_character(character)
