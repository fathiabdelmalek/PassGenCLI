from datetime import datetime

import json
import os


class History:
    def __init__(self):
        if not os.path.exists(os.path.expanduser("~/.config/pass-gen")):
            os.mkdir(f"{os.path.expanduser('~')}/.config/pass-gen")
        self._file = os.path.expanduser("~/.config/pass-gen/history.json")
        self._history = []

    @property
    def history(self):
        return self._history

    def load_history(self):
        if os.path.exists(self._file):
            with open(self._file, "r") as f:
                try:
                    self._history = json.load(f)
                except json.JSONDecodeError:
                    self._history = []
            return self._history
        return []

    def save_history(self):
        with open(self._file, "w") as f:
            json.dump(self._history, f, indent=4)

    def add_to_history(self, text, key, password):
        entry = {
            "text": text,
            "key": key,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._history.append(entry)
        self.save_history()

    def clear_history(self):
        self._history.clear()
        self.save_history()
