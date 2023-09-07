#!/bin/python3
from passgencli.config import Config
from passgencli.generator import Generator
from passgencli.interface import Interface
from passgencli.parser import args


config = Config()
generator = Generator()
interface = Interface()


def generate_password(text):
    key = args.key if args.key else interface.get_key()
    password = generator.generate_password(text, key)
    interface.display_result(text, key, password)
    interface.copy_to_clipboard(password)


def replace_character(character, replacement):
    generator.replace_character(character, replacement)
    config.set_setting(config.characters_replacements, character, replacement)
    config.save_config()


def reset_character(character):
    generator.reset_character(character)
    config.del_setting(config.characters_replacements, character)
    config.save_config()


def main():
    config.load_config()
    characters = config.get_settings(config.characters_replacements)
    for key, value in characters.items():
        generator.replace_character(key, value)
    if args.command == 'config':
        if args.replace:
            character, replacement = args.replace
            replace_character(character[0], replacement)
        if args.reset:
            character = args.reset[0]
            reset_character(character[0])
        return
    if args.command == 'generate':
        text = " ".join(args.text) if args.text else interface.get_text()
        generate_password(text)
        return
    while True:
        print("=" * 64)
        choice = interface.display_menu()
        match choice:
            case 1:
                text = interface.get_text()
                generate_password(text)
            case 2:
                character, replacement = interface.replace_character()
                replace_character(character, replacement)
            case 3:
                character = interface.reset_character()
                reset_character(character)
            case 0:
                break
        print("=" * 64)


if __name__ == '__main__':
    main()
