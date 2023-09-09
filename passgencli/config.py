from configparser import ConfigParser
import os


class Config:
    def __init__(self):
        if not os.path.exists(os.path.expanduser("~/.config/pass-gen")):
            os.mkdir(f"{os.path.expanduser('~')}/.config/pass-gen")
        self._file = os.path.expanduser("~/.config/pass-gen/settings.conf")
        self._characters_replacements = "Characters Replacements"
        self._history = "History"
        self._config = ConfigParser()

    @property
    def config(self):
        return self._config

    @property
    def characters_replacements(self):
        return self._characters_replacements

    @property
    def history(self):
        return self._history

    def load_config(self):
        if os.path.exists(self._file):
            self._config.read(self._file)

    def save_config(self):
        with open(self._file, 'w') as configfile:
            self._config.write(configfile)

    def get_key(self, section, key, default=None):
        return self._config.get(section, key, fallback=default)

    def set_key(self, section, key, value):
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, value)

    def del_key(self, section, key):
        self._config.remove_option(section, key)

    def del_section(self, section):
        self._config.remove_section(section)

    def get_settings(self, section):
        items = {}
        if self._config.has_section(section):
            for key, value in self._config.items(section):
                items[key] = value
        return items
