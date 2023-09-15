from .config import Config
from .generator import Generator
from .history import History
from .interface import Interface
from .logger import Logger
from .parser import Parser


class PasswordCLI:
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
        self._interface.display_result(text, key, password)
        self._interface.copy_to_clipboard(password)
        self._logger.log_info("new password generated")
        if context:
            self._history.add_to_history(text, key, password, context)
            self._logger.log_info("password saved on history")

    def get_password(self, context):
        try:
            self._interface.display_result(context['text'], context['key'], context['password'])
            self._interface.copy_to_clipboard(context['password'])
            self._logger.log_info("retrieved saved password")
        except TypeError:
            self._interface.display_error(context)
            self._logger.log_error(f"entered unsaved password context {context}")

    def replace_character(self, character, replacement):
        try:
            self._generator.replace_character(character, replacement)
            self._config.set_key(self._config.characters_replacements, character, replacement)
            self._config.save_config()
            self._logger.log_info(f"replace character {character} with {replacement}")
        except ValueError:
            print(f"'{replacement}' is not a valid replacement, you should chose another replacement")
            self._logger.log_error(f"failed to set character '{character}' replacement with '{replacement}'")

    def reset_character(self, character):
        self._generator.reset_character(character)
        self._config.del_key(self._config.characters_replacements, character)
        self._config.save_config()
        self._logger.log_info(f"reset character {character} to its default")
        
    def display_hello_message(self):
        self._interface.display_hello_message()

    def display_exit_message(self):
        self._interface.display_exit_message()
