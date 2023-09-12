import logging
import os
from datetime import datetime


class Logger:
    def __init__(self):
        log_file = os.path.join(os.path.expandvars("$XDG_CACHE_HOME/pass-gen"),
                                f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_file,
            filemode="a",
        )

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)

    def log_exception(self, message):
        logging.exception(message)
