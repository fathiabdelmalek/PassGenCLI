#!/bin/python3
from core import PassGenCLI
import os
import platform

version = "0.11.0"


def setup_xdg_variables():
    xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    xdg_data_home = os.environ.get("XDG_DATA_HOME")

    if xdg_cache_home is None:
        xdg_cache_home = os.path.expanduser("~/.cache")
        os.environ["XDG_CACHE_HOME"] = xdg_cache_home

    if xdg_config_home is None:
        xdg_config_home = os.path.expanduser("~/.config")
        os.environ["XDG_CONFIG_HOME"] = xdg_config_home

    if xdg_data_home is None:
        xdg_data_home = os.path.expanduser("~/.local/share")
        os.environ["XDG_DATA_HOME"] = xdg_data_home


def setup_paths(platform_name):
    paths = {
        "Windows": {
            "cache": os.path.expanduser(os.path.join("~", ".passgen")),
            "config": os.path.expanduser(os.path.join("~", ".passgen")),
            "data": os.path.expanduser(os.path.join("~", ".passgen")),
        },
        "Linux": {
            "cache": os.path.expandvars(os.path.join("$XDG_CACHE_HOME", "passgen")),
            "config": os.path.expandvars(os.path.join("$XDG_CONFIG_HOME", "passgen")),
            "data": os.path.expandvars(os.path.join("$XDG_DATA_HOME", "passgen")),
        },
        "Darwin": {
            "cache": os.path.expanduser(os.path.join("~", "Library", "Caches", "passgen")),
            "config": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passgen")),
            "data": os.path.expanduser(os.path.join("~", "Library", "Application Support", "passgen")),
        }
    }

    if platform_name not in paths:
        raise Exception("Unsupported platform")

    return paths[platform_name]


def create_dirs(paths):
    for path in paths.values():
        if not os.path.exists(path):
            os.makedirs(path)


def manage_passwords(app):
    if app.args.command:
        match app.args.command:
            case 'generate':
                app.generate_password(" ".join(app.args.text) if app.args.text else app.interface.get_text(),
                                      app.args.key if app.args.key else app.interface.get_key(),
                                      app.config.get_key(app.config.encryption_method, 'shift', 5),
                                      " ".join(app.args.context) if app.args.context else app.interface.get_context_to_save())
            case 'update':
                app.update_password(" ".join(app.args.context if app.args.context else app.interface.get_context_to_load()),
                                    " ".join(app.args.text) if app.args.text else app.interface.get_text_to_update(),
                                    app.args.key if app.args.key else app.interface.get_key(True))
            case 'remove':
                app.remove_password(" ".join(app.args.context))


def manage_config(app):
    if app.args.command:
        match app.args.command:
            case 'shift':
                app.change_shift(app.args.shift[0])
            case 'reset_shift':
                app.reset_shift()
            case 'replace':
                app.replace_character(app.args.character[0][0], app.args.replacement[0])
            case 'reset_rep':
                app.reset_character(app.args.character[0][0])
            case 'char_rep':
                app.show_character_replacement(str(app.args.character[0]))
            case 'all_reps':
                app.show_all_characters_replacements()


def manage_history(app):
    if app.args.command:
        match app.args.command:
            case 'get':
                app.get_password(" ".join(app.args.context))
            case 'show_all':
                app.show_all_passwords()
            case 'clear':
                app.history.clear_history()
            case 'save_backup':
                pass
            case 'load_backup':
                pass
            case 'encrypt':
                pass
            case 'decrypt':
                pass


def main_loop():
    while True:
        print("=" * 64)
        main_choice = app.interface.display_main_menu()
        match main_choice:
            case 1:
                choice = app.interface.display_passwords_menu()
                match choice:
                    case 1:
                        continue
                    case 2:
                        app.generate_password(app.interface.get_text(),
                                              app.interface.get_key(),
                                              app.config.get_key(app.config.encryption_method, 'shift', 5),
                                              app.interface.get_context_to_save())
                    case 3:
                        app.update_password(app.interface.get_context_to_load(),
                                            app.interface.get_text_to_update(),
                                            app.interface.get_key(True))
                    case 4:
                        app.remove_password(app.interface.get_context_to_load())
                    case 0:
                        break
            case 2:
                choice = app.interface.display_config_menu()
                match choice:
                    case 1:
                        continue
                    case 2:
                        app.change_shift(app.interface.get_shift())
                    case 3:
                        app.reset_shift()
                    case 4:
                        app.replace_character(*app.interface.replace_character())
                    case 5:
                        app.reset_character(app.interface.reset_character())
                    case 6:
                        app.show_character_replacement(app.interface.get_character())
                    case 7:
                        app.show_all_characters_replacements()
                    case 0:
                        break
            case 3:
                choice = app.interface.display_history_menu()
                match choice:
                    case 1:
                        continue
                    case 2:
                        app.get_password(app.interface.get_context_to_load())
                    case 3:
                        app.show_all_passwords()
                    case 4:
                        app.history.clear_history()
                    case 5:
                        continue
                    case 6:
                        continue
                    case 7:
                        continue
                    case 8:
                        continue
                    case 0:
                        break
            case 0:
                break
        print("=" * 64)


def main(app):
    if app.args.section:
        match app.args.section:
            case 'passwords':
                manage_passwords(app)
            case 'config':
                manage_config(app)
            case 'history':
                manage_history(app)
        return
    main_loop()


if __name__ == '__main__':
    platform_name = platform.system()
    paths = setup_paths(platform_name)
    if platform_name == 'Linux':
        setup_xdg_variables()
    create_dirs(paths)
    app = PassGenCLI(paths["cache"], paths["config"], paths["data"], version)
    app.interface.display_hello_message()
    try:
        main(app)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    app.interface.display_exit_message()
