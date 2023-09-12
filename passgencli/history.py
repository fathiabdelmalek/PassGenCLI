from datetime import datetime

import json
import os


class History:
    def __init__(self):
        self._file = os.path.expanduser("~/.pass-gen/history.json")
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

    def add_to_history(self, text, key, password, context=None):
        entry = {
            "text": text,
            "key": key,
            "context": context,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        existing_entry = None
        for i, history_entry in enumerate(self._history):
            if history_entry["context"] == context:
                existing_entry = i
                break
        if existing_entry is not None:
            self._history[existing_entry] = entry
        else:
            self._history.append(entry)
        self.save_history()

    def clear_history(self):
        self._history.clear()
        self.save_history()

    def get_password(self, context):
        for entry in self._history:
            if entry['context'] == context:
                return entry
        return context
