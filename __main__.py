#!/bin/python3
from passgencli.password_cli import PasswordCLI
import os
import platform

version = "1.5.0"


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
            "cache": os.path.expanduser("~/.pass-gen"),
            "config": os.path.expanduser("~/.pass-gen"),
            "data": os.path.expanduser("~/.pass-gen"),
        },
        "Linux": {
            "cache": os.path.expandvars("$XDG_CACHE_HOME/pass-gen"),
            "config": os.path.expandvars("$XDG_CONFIG_HOME/pass-gen"),
            "data": os.path.expandvars("$XDG_DATA_HOME/pass-gen"),
        }
    }

    if platform_name not in paths:
        raise Exception("Unsupported platform")

    return paths[platform_name]


def create_dirs(paths):
    for path in paths.values():
        if not os.path.exists(path):
            os.makedirs(path)


def main(app):
    if app.args.command:
        match app.args.command:
            case 'generate':
                app.generate_password(" ".join(app.args.text) if app.args.text else app.interface.get_text(),
                                      app.args.key if app.args.key else app.interface.get_key(),
                                      " ".join(app.args.context) if app.args.context else app.interface.get_context_to_save())
            case 'get':
                app.get_password(" ".join(app.args.context))
            case 'remove':
                app.remove_password(" ".join(app.args.context))
            case 'replace':
                app.replace_character(app.args.character[0][0], str(app.args.replacement[0]))
            case 'reset':
                app.reset_character(app.args.character[0][0])
            case 'clear':
                app.history.clear_history()
        return

    while True:
        print("=" * 64)
        choice = app.interface.display_menu()
        match choice:
            case 1:
                app.generate_password(app.interface.get_text(), app.interface.get_key(),
                                      app.interface.get_context_to_save())
            case 2:
                app.get_password(app.interface.get_context_to_load())
            case 3:
                app.remove_password(app.interface.get_context_to_load())
            case 4:
                app.replace_character(*app.interface.replace_character())
            case 5:
                app.reset_character(app.interface.reset_character())
            case 6:
                app.history.clear_history()
            case 0:
                break
        print("=" * 64)


if __name__ == '__main__':
    platform_name = platform.system()
    setup_xdg_variables()
    paths = setup_paths(platform_name)
    create_dirs(paths)
    app = PasswordCLI(paths["cache"], paths["config"], paths["data"], version)
    characters = app.config.get_settings(app.config.characters_replacements)
    for key, value in characters.items():
        app.generator.replace_character(key, value)
    app.display_hello_message()
    try:
        main(app)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    app.display_exit_message()
