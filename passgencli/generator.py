from passwords_generator import PasswordGenerator


class Generator:
    def __init__(self):
        self.generator = PasswordGenerator()
        
    def generate_password(self, plain_text, key_phrase):
        self.generator.plain_text = plain_text
        self.generator.key_phrase = key_phrase
        password = self.generator.generate_password()
        return password

    def replace_character(self, character, replacement):
        self.generator.replace_character(character, replacement)

    def reset_character(self, character):
        self.generator.reset_character(character)
