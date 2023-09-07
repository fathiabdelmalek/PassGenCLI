from passwords_generator import PasswordGenerator


class Generator:
    def __init__(self):
        self.generator = PasswordGenerator()
        
    def generate_password(self, text, key):
        password = self.generator.generate_password(text, key)
        return password

    def replace_character(self, character, replacement):
        self.generator.replace_character(character, replacement)

    def reset_character(self, character):
        self.generator.reset_character(character)
