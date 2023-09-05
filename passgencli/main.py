#!/bin/python3
from passwords_generator import PasswordGenerator

from passgencli.parser import args
from passgencli.user_interface import UserInterface


def main():
    user_interface = UserInterface()
    password_generator = PasswordGenerator()
    password_generator.plain_text = " ".join(args.text) if args.text else ""
    password_generator.key_phrase = args.key if args.key else ""
    with_matrix = args.matrix if args.matrix else None
    while True:
        choice = user_interface.display_menu()
        match choice:
            case 1:
                if password_generator.plain_text == "":
                    password_generator.plain_text = user_interface.get_plain_text()
                if password_generator.key_phrase == "":
                    password_generator.key_phrase = user_interface.get_key_phrase()
                with_matrix = with_matrix if with_matrix else True if input(
                    "Do you want to see the used matrix? (y/N): ").lower() == 'y' else False
                password = password_generator.generate_password()
                matrix = []
                if with_matrix:
                    for row in password_generator.matrix:
                        matrix.append(row)
                user_interface.display_result(password_generator, password, matrix)
                user_interface.copy_to_clipboard(password)
                password_generator.plain_text = ""
                password_generator.key_phrase = ""
                with_matrix = None
            case 2:
                character, replacement = user_interface.replace_character()
                password_generator.replace_character(character, replacement)
            case 3:
                password_generator.reset_character(user_interface.reset_character())
            case 0:
                break


if __name__ == '__main__':
    main()
