from .config import Config
from .generator import Generator
from .history import History
from .interface import Interface
from .logger import Logger
from .parser import Parser


class PassGenCLI:
    def __init__(self, cache_path, config_path, data_path, version):
        self._config = Config(config_path)
        self._generator = Generator()
        self._history = History(data_path)
        self._interface = Interface()
        self._logger = Logger(cache_path)
        self._args = Parser(version).parse_args()
        self._config.load_config()
        self._history.load_history()
        for key, value in self._config.get_settings(self._config.characters_replacements).items():
            self._generator.replace_character(key, value)

    @property
    def config(self):
        return self._config

    @property
    def generator(self):
        return self._generator

    @property
    def history(self):
        return self._history

    @property
    def interface(self):
        return self._interface

    @property
    def logger(self):
        return self._logger

    @property
    def args(self):
        return self._args

    def generate_password(self, text, key, context):
        password = self._generator.generate_password(text, key)
        self._interface.display_password(text, key, password)
        self._interface.copy_to_clipboard(password)
        self._logger.log_info("new password generated")
        if context:
            self._history.add_to_history(text, key, password, context)
            self._logger.log_info("password saved on history")

    def get_password(self, context):
        entry = self._history.get_password(context)
        if entry is not None:
            self._interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
            self._interface.copy_to_clipboard(entry['password'])
            self._logger.log_info("saved password was retrieved")
            return
        self._interface.display_context_error_message(context)
        self._logger.log_error(f"entered unsaved password context {context}")

    def update_password(self, context, _text, _key):
        entry = self._history.get_password(context)
        if entry is not None:
            text = _text if _text is not None else entry['text']
            key = _key if _key is not None else entry['key']
            password = self._generator.generate_password(text, key)
            self._interface.display_password(text, key, password)
            self._interface.copy_to_clipboard(password)
            self._history.update_password(context, text, key, password)
            self._logger.log_info("password updated successfully")
            self._history.save_history()
            self._logger.log_info("password saved on history")
            return
        self._interface.display_context_error_message(context)
        self._logger.log_error(f"entered unsaved password context {context}")

    def remove_password(self, context):
        entry = self._history.get_password(context)
        if self._history.remove_password(context):
            self._interface.display_password_removed_message()
            self._interface.display_password(entry['text'], entry['key'], entry['password'], entry['context'])
            self._logger.log_warning("saved password was remover")
        else:
            self._interface.display_context_error_message(context)
            self._logger.log_error(f"entered unsaved password context {context}")

    def replace_character(self, character, replacement):
        try:
            if replacement in ['`', '~', '#', '%', '&', '*' '(', ')', '<', '>', '?', ';', '\'', '"', '|', '\\']:
                raise ValueError
            self._generator.replace_character(character, replacement)
            self._config.set_key(self._config.characters_replacements, character, replacement)
            self._config.save_config()
            self._logger.log_info(f"replace character {character} with {replacement}")
        except ValueError:
            self._interface.display_replacement_error_message(replacement)
            self._logger.log_error(f"failed to set character '{character}' replacement with '{replacement}'")

    def reset_character(self, character):
        self._generator.reset_character(character)
        self._config.del_key(self._config.characters_replacements, character)
        self._config.save_config()
        self._logger.log_info(f"reset character {character} to its default")

    def show_all_passwords(self):
        for password in self._history.history:
            self._interface.display_password(password['text'], password['key'], password['password'], password['context'])
            print()

    def show_character_replacement(self, char):
        rep = self._config.get_key(self._config.characters_replacements, char)
        if rep is not None:
            self._interface.display_character_replacement(char, rep)

    def show_all_characters_replacements(self):
        chars = self._config.get_settings(self._config.characters_replacements)
        for char, rep in chars.items():
            self._interface.display_character_replacement(char, rep)




__all__ = ['PassGenCLI']
