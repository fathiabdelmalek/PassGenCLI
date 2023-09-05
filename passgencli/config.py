import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.file = os.path.expanduser("~/.config/passgencli.conf")
        self._characters_replacements = "Characters Replacements"

    @property
    def characters_replacements(self):
        return self._characters_replacements

    def load_config(self):
        if os.path.exists(self.file):
            self.config.read(self.file)

    def get_setting(self, section, key, default=None):
        return self.config.get(section, key, fallback=default)

    def set_setting(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def del_setting(self, section, key):
        self.config.remove_option(section, key)

    def get_settings(self, section):
        items = {}
        if self.config.has_section(section):
            for key, value in self.config.items(section):
                items[key] = value
        return items

    def save_config(self):
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)
