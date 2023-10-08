#!/bin/python3
from core import PassGenCLI
import os
import platform

version = "0.9.0"


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
            "cache": os.path.expanduser(os.path.join("~", ".pass-gen")),
            "config": os.path.expanduser(os.path.join("~", ".pass-gen")),
            "data": os.path.expanduser(os.path.join("~", ".pass-gen")),
        },
        "Linux": {
            "cache": os.path.expandvars(os.path.join("$XDG_CACHE_HOME", "pass-gen")),
            "config": os.path.expandvars(os.path.join("$XDG_CONFIG_HOME", "pass-gen")),
            "data": os.path.expandvars(os.path.join("$XDG_DATA_HOME", "pass-gen")),
        },
        "Darwin": {
            "cache": os.path.expanduser(os.path.join("~", "Library", "Caches", "pass-gen")),
            "config": os.path.expanduser(os.path.join("~", "Library", "Application Support", "pass-gen")),
            "data": os.path.expanduser(os.path.join("~", "Library", "Application Support", "pass-gen")),
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
                                      " ".join(
                                          app.args.context) if app.args.context else app.interface.get_context_to_save())
            case 'get':
                app.get_password(" ".join(app.args.context))
        return


def manage_config(app):
    if app.args.command:
        match app.args.command:
            case 'replace':
                app.replace_character(app.args.character[0][0], str(app.args.replacement[0]))
            case 'reset':
                app.reset_character(app.args.character[0][0])
        return

def manage_history(app):
    if app.args.command:
        match app.args.command:
            case 'show_all':
                pass
            case 'clear':
                app.history.clear_history()
        return


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
                        app.generate_password(app.interface.get_text(), app.interface.get_key(),
                                              app.interface.get_context_to_save())
                    case 3:
                        app.get_password(app.interface.get_context_to_load())
                    case 4:
                        pass  # update password
                    case 5:
                        app.remove_password(app.interface.get_context_to_load())
                    case 0:
                        break
            case 2:
                choice = app.interface.display_config_menu()
                match choice:
                    case 1:
                        continue
                    case 2:
                        app.replace_character(*app.interface.replace_character())
                    case 3:
                        app.reset_character(app.interface.reset_character())
                    case 4:
                        pass
                    case 5:
                        pass
                    case 6:
                        pass
                    case 7:
                        pass
                    case 8:
                        pass
                    case 0:
                        break
            case 3:
                choice = app.interface.display_history_menu()
                match choice:
                    case 1:
                        continue
                    case 2:
                        pass
                    case 3:
                        app.history.clear_history()
                    case 4:
                        pass
                    case 5:
                        pass
                    case 0:
                        break
            case 0:
                break
        print("=" * 64)


if __name__ == '__main__':
    platform_name = platform.system()
    setup_xdg_variables()
    paths = setup_paths(platform_name)
    create_dirs(paths)
    app = PassGenCLI(paths["cache"], paths["config"], paths["data"], version)
    characters = app.config.get_settings(app.config.characters_replacements)
    for key, value in characters.items():
        app.generator.replace_character(key, value)
    app.interface.display_hello_message()
    try:
        main(app)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    app.interface.display_exit_message()
