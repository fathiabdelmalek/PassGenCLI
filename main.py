#!/bin/python3
from passgencli import Config, Generator, History, Interface, Logger, Parser

import os


if not os.path.exists(os.path.expanduser("~/.pass-gen")):
    os.mkdir(f"{os.path.expanduser('~')}/.pass-gen")

config = Config()
generator = Generator()
history = History()
interface = Interface()
logger = Logger()
args = Parser().parse_args()


def generate_password(text, key, context):
    password = generator.generate_password(text, key)
    interface.display_result(text, key, password)
    interface.copy_to_clipboard(password)
    logger.log_info("new password generated")
    if context:
        history.add_to_history(text, key, password, context)
        logger.log_info("password saved on history")


def get_password(context):
    try:
        interface.display_result(context['text'], context['key'], context['password'])
        interface.copy_to_clipboard(context['password'])
        logger.log_info("retrieved saved password")
    except TypeError:
        interface.display_error(context)
        logger.log_error(f"entered unsaved password context {context}")


def replace_character(character, replacement):
    try:
        generator.replace_character(character, replacement)
        config.set_key(config.characters_replacements, character, replacement)
        config.save_config()
        logger.log_info(f"replace character {character} with {replacement}")
    except ValueError:
        print(f"'{replacement}' is not a valid replacement, you should chose another replacement")
        logger.log_error(f"failed to set character '{character}' replacement with '{replacement}'")


def reset_character(character):
    generator.reset_character(character)
    config.del_key(config.characters_replacements, character)
    config.save_config()
    logger.log_info(f"reset character {character} to its default")


def main():
    config.load_config()
    history.load_history()
    characters = config.get_settings(config.characters_replacements)
    for key, value in characters.items():
        generator.replace_character(key, value)
    if args.command == 'generate':
        generate_password(" ".join(args.text) if args.text else interface.get_text(),
                          args.key if args.key else interface.get_key(),
                          args.context if args.context else interface.get_context_to_save())
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
                generate_password(interface.get_text(), interface.get_key(), interface.get_context_to_save())
            case 2:
                get_password(history.get_password(interface.get_context_to_load()))
            case 3:
                replace_character(*interface.replace_character())
            case 4:
                reset_character(interface.reset_character())
            case 5:
                history.clear_history()
            case 0:
                break
        print("=" * 64)


if __name__ == '__main__':
    interface.display_hello_message()
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    interface.display_exit_message()
