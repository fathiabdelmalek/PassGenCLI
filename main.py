#!/bin/python3
from passgencli import Config, Generator, History, Interface, Parser

config = Config()
generator = Generator()
history = History()
interface = Interface()
args = Parser().parse_args()


def generate_password(text, key):
    password = generator.generate_password(text, key)
    interface.display_result(text, key, password)
    interface.copy_to_clipboard(password)
    context = interface.save_context()
    if context:
        history.add_to_history(text, key, password, context)


def get_password(entry):
    if entry:
        interface.display_result(entry['text'], entry['key'], entry['password'])
        interface.copy_to_clipboard(entry['password'])
        return
    interface.display_error(entry)


def replace_character(character, replacement):
    generator.replace_character(character, replacement)
    config.set_key(config.characters_replacements, character, replacement)
    config.save_config()


def reset_character(character):
    generator.reset_character(character)
    config.del_key(config.characters_replacements, character)
    config.save_config()


def main():
    config.load_config()
    history.load_history()
    characters = config.get_settings(config.characters_replacements)
    for key, value in characters.items():
        generator.replace_character(key, value)
    if args.command == 'generate':
        generate_password(" ".join(args.text) if args.text else interface.get_text(),
                          args.key if args.key else interface.get_key())
        return
    if args.command == 'get':
        get_password(history.get_password(args.context[0]))
        return
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
    while True:
        print("=" * 64)
        choice = interface.display_menu()
        match choice:
            case 1:
                generate_password(interface.get_text(), interface.get_key())
            case 2:
                get_password(history.get_password(interface.get_context()))
            case 3:
                replace_character(*interface.replace_character())
            case 4:
                reset_character(interface.reset_character())
            case 5:
                history.clear_history()
            case 0:
                print("Program exit")
                break
        print("=" * 64)


if __name__ == '__main__':
    import os
    if not os.path.exists(os.path.expandvars("$XDG_CACHE_HOME/pass-gen")):
        os.mkdir(f"{os.path.expandvars('$XDG_CACHE_HOME')}/pass-gen")
    if not os.path.exists(os.path.expandvars("$XDG_CONFIG_HOME/pass-gen")):
        os.mkdir(f"{os.path.expandvars('$XDG_CONFIG_HOME')}/pass-gen")
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram exit")
