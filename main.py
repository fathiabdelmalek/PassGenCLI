#!/bin/python3
from passgencli.password_cli import PasswordCLI
import os
import platform

match platform.system():
    case "Windows":
        from ctypes import windll  # Only exists on Windows.
        app_id = 'fathi.pass-gen'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        cache_path = os.path.expanduser("~/.pass-gen")
        config_path = os.path.expanduser("~/.pass-gen")
        data_path = os.path.expanduser("~/.pass-gen")
    case "Linux":
        xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        xdg_data_home = os.environ.get("XDG_DATA_HOME")
        bash_profile_path = os.path.expanduser("~/.bash_profile")
        with open(bash_profile_path, "a") as bash_profile:
            if xdg_cache_home is None:
                xdg_cache_home = os.path.expanduser("~/.cache")
                os.environ["XDG_CACHE_HOME"] = xdg_cache_home
                bash_profile.write(f'export XDG_CACHE_HOME="{xdg_cache_home}"\n')
            if xdg_config_home is None:
                xdg_config_home = os.path.expanduser("~/.config")
                os.environ["XDG_CONFIG_HOME"] = xdg_config_home
                bash_profile.write(f'export XDG_CONFIG_HOME="{xdg_config_home}"\n')
            if xdg_data_home is None:
                xdg_data_home = os.path.expanduser("~/.local/share")
                os.environ["XDG_DATA_HOME"] = xdg_data_home
                bash_profile.write(f'export XDG_DATA_HOME="{xdg_data_home}"\n')
        cache_path = os.path.expandvars("$XDG_CACHE_HOME/pass-gen")
        config_path = os.path.expandvars("$XDG_CONFIG_HOME/pass-gen")
        data_path = os.path.expandvars("$XDG_DATA_HOME/pass-gen")
    case _:
        exit(1)
if not os.path.exists(cache_path):
    os.makedirs(cache_path)
if not os.path.exists(config_path):
    os.makedirs(config_path)
if not os.path.exists(data_path):
    os.makedirs(data_path)

app = PasswordCLI(cache_path, config_path, data_path)
app.display_hello_message()
try:
    characters = app.config.get_settings(app.config.characters_replacements)
    for key, value in characters.items():
        app.generator.replace_character(key, value)
    if app.args.command == 'generate':
        app.generate_password(" ".join(app.args.text) if app.args.text else app.interface.get_text(),
                              app.args.key if app.args.key else app.interface.get_key(),
                              app.args.context if app.args.context else app.interface.get_context_to_save())
        exit(0)
    if app.args.command == 'get':
        app.get_password(app.history.get_password(app.args.context[0]))
        exit(0)
    if app.args.command == 'config':
        if app.args.replace:
            character, replacement = app.args.replace
            app.replace_character(character[0], replacement)
        if app.args.reset:
            character = app.args.reset[0]
            app.reset_character(character[0])
        if app.args.clear:
            app.history.clear_history()
        exit(0)
    while True:
        print("=" * 64)
        choice = app.interface.display_menu()
        match choice:
            case 1:
                app.generate_password(app.interface.get_text(), app.interface.get_key(),
                                      app.interface.get_context_to_save())
            case 2:
                app.get_password(app.history.get_password(app.interface.get_context_to_load()))
            case 3:
                app.replace_character(*app.interface.replace_character())
            case 4:
                app.reset_character(app.interface.reset_character())
            case 5:
                app.history.clear_history()
            case 0:
                break
        print("=" * 64)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
app.display_exit_message()
