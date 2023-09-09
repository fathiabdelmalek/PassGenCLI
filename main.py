#!/bin/python3
from passgencli.config import Config
from passgencli.history import History
from passgencli.generator import Generator
from passgencli.interface import Interface
from passgencli.parser import Parser


config = Config()
history = History()
generator = Generator()
interface = Interface()
args = Parser().parse_args()


def generate_password(text, key):
    password = generator.generate_password(text, key)
    history.add_to_history(text, key, password)
    interface.display_result(text, key, password)
    interface.copy_to_clipboard(password)


def replace_character(character, replacement):
    generator.replace_character(character, replacement)
    config.set_key(config.characters_replacements, character, replacement)
    config.save_config()


def reset_character(character):
    generator.reset_character(character)
    config.del_key(config.characters_replacements, character)
    config.save_config()


def main():
    history.load_history()
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
        if args.clear:
            history.clear_history()
        return
    if args.command == 'generate':
        generate_password(" ".join(args.text) if args.text else interface.get_text(),
                          args.key if args.key else interface.get_key())
        return
    while True:
        print("=" * 64)
        choice = interface.display_menu()
        match choice:
            case 1:
                generate_password(interface.get_text(), interface.get_key())
            case 2:
                replace_character(*interface.replace_character())
            case 3:
                reset_character(interface.reset_character())
            case 4:
                history.clear_history()
            case 0:
                break
        print("=" * 64)


if __name__ == '__main__':
    main()
