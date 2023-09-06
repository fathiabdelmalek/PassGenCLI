#!/bin/python3
from passgencli.config import Config
from passgencli.generator import Generator
from passgencli.interface import Interface
from passgencli.parser import args


def generate_password(interface, generator, plain_text):
    key_phrase = args.key if args.key else interface.get_key_phrase()
    password = generator.generate_password(plain_text, key_phrase)
    interface.display_result(plain_text, key_phrase, password)
    interface.copy_to_clipboard(password)


def main():
    config = Config()
    generator = Generator()
    interface = Interface()
    config.load_config()
    characters = config.get_settings(config.characters_replacements)
    for key, value in characters.items():
        generator.replace_character(key, value)
    if args.command == 'config':
        if args.replace:
            character, replacement = args.replace
            character = character[0]
            generator.replace_character(character, replacement)
            config.set_setting(config.characters_replacements, character, replacement)
            config.save_config()
            return
        if args.reset:
            character = args.reset[0]
            character = character[0]
            generator.reset_character(character)
            config.del_setting(config.characters_replacements, character)
            config.save_config()
            return
    if args.command == 'generate':
        plain_text = " ".join(args.text) if args.text else ""
        if plain_text != "":
            generate_password(interface, generator, plain_text)
            return
        while True:
            print("=" * 64)
            choice = interface.display_menu()
            match choice:
                case 1:
                    plain_text = plain_text if plain_text != "" else interface.get_plain_text()
                    generate_password(interface, generator, plain_text)
                    plain_text = ""
                case 2:
                    character, replacement = interface.replace_character()
                    generator.replace_character(character, replacement)
                    config.set_setting(config.characters_replacements, character, replacement)
                    config.save_config()
                case 3:
                    character = interface.reset_character()
                    generator.reset_character(character)
                    config.del_setting(config.characters_replacements, character)
                    config.save_config()
                case 0:
                    break
            print("=" * 64)


if __name__ == '__main__':
    main()
