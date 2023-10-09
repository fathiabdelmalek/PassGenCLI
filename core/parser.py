from argparse import ArgumentParser, Namespace


class Parser:
    def __init__(self, version):
        self._parser = ArgumentParser(prog="passgen",
                                      description="Strong passwords generator with Playfair cypher algorithm")
        self._parser.epilog = "Run pass-gen <command> --help for more information on a command."
        self._parser.add_argument("-v", "--version", action="version", version=f'%(prog)s {version}',
                                  help="Print version information and exit")
        self._sp = self._parser.add_subparsers(title="Sections", dest="section",
                                               description="Choose a command to manage passwords, configure settings, or access history.")
        # passwords
        passwords_manager_parser = self._sp.add_parser("passwords", help="Manage passwords.")
        self._passwords_management_subparsers = passwords_manager_parser.add_subparsers(title="Password Management Commands",
                                                                                        dest="command")
        # config
        config_manager_parser = self._sp.add_parser("config", help="Manage program configurations.")
        self._config_management_subparsers = config_manager_parser.add_subparsers(title="Configurations Management Commands",
                                                                            dest="command")
        # history
        history_manager_parser = self._sp.add_parser("history", help="Access history.")
        self._history_management_subparsers = history_manager_parser.add_subparsers(title="History Management Commands",
                                                                              dest="command")
        self._make_passwords_management_parser()
        self._make_config_management_parser()
        self._make_history_management_parser()

    def _make_passwords_management_parser(self):
        # generate password parser
        generate_parser = self._passwords_management_subparsers.add_parser("generate",
                                                                     help="Generate passwords from text and key",
                                                                     description="Generate passwords from text and key")
        generate_parser.add_argument("-t", "--text", nargs='+', help="The plain text you want to encode")
        generate_parser.add_argument("-k", "--key", help="The key phrase")
        generate_parser.add_argument("-c", "--context", nargs='+',
                                     help="The context if you want to save the password on history")
        generate_parser.epilog = "Example: pass-gen generate -t 'my text' -k 'my_key' -c 'my context'"
        # update password parser
        update_password_parser = self._passwords_management_subparsers.add_parser("update",
                                                                            help="Update saved password with new text",
                                                                            description="Update saved password with new text")
        update_password_parser.add_argument("-c", "--context", nargs='+', help="The context of the saved password")
        update_password_parser.add_argument("-t", "--text", nargs='+', help="The new plain text to encode")
        update_password_parser.add_argument("-k", "--key", nargs='?', help="The key phrase if you want to change it too")
        update_password_parser.epilog = "Example: passgen passwords update -c 'my context' -t 'my new text' -k 'my new key'"
        # remove password parser
        remove_password_parser = self._passwords_management_subparsers.add_parser("remove",
                                                                            help="Remove save password from history",
                                                                            description="Remove save password from history")
        remove_password_parser.add_argument("context", nargs='+', help="The context of the saved password")
        remove_password_parser.epilog = "Example: pass-gen passwords remove 'my context'"

    def _make_config_management_parser(self):
        # replace character parser
        replace_character_parser = self._config_management_subparsers.add_parser("replace",
                                                                           help="Replace one character with a set of characters after cipher",
                                                                           description="Replace one character with a set of characters after cipher")
        replace_character_parser.add_argument("character",
                                              help="Character to be replaced (should be one character)")
        replace_character_parser.add_argument("replacement", nargs=1,
                                              help="The replacement string (should not contain spaces)")
        replace_character_parser.epilog = "Example: pass-gen replace e '1@2#"
        # reset character parser
        reset_character_parser = self._config_management_subparsers.add_parser("reset",
                                                                         help="Reset a character to it's default value",
                                                                         description="Reset a character to it's default value")
        reset_character_parser.add_argument("character", nargs=1, help="Character to reset it")
        reset_character_parser.epilog = "Example: passgen reset e"
        # show replacements parser
        self._config_management_subparsers.add_parser("show_replacements",
                                                help="Show all characters replacements",
                                                description="Show all characters replacements")

    def _make_history_management_parser(self):
        # get password parser
        get_password_parser = self._history_management_subparsers.add_parser("get",
                                                                         help="Retrieve a saved password by it's context",
                                                                         description="Retrieve a saved password by it's context")
        get_password_parser.add_argument("context", nargs='+', help="The context of the saved password")
        get_password_parser.epilog = "Example: pass-gen get 'my context'"
        # show all passwords parser
        self._history_management_subparsers.add_parser("show_all", help="Show All saved passwords",
                                                 description="Show All saved passwords")
        # clear history parser
        self._history_management_subparsers.add_parser("clear", help="Clear the history",
                                                 description="Clear the history")
        # save backup history parser
        save_backup_history_parser = self._history_management_subparsers.add_parser("save_backup",
                                                                         help="Backup history to backup file",
                                                                         description="Backup history to backup file")
        save_backup_history_parser.add_argument("file", nargs=1, help="The file name to backup the data on")
        # load backup history parser
        load_backup_history_parser = self._history_management_subparsers.add_parser("load_backup",
                                                                                  help="Retrieve history from backup file",
                                                                                  description="Retrieve history from backup file")
        load_backup_history_parser.add_argument("file", nargs=1, help="The backup file name to get data from")

    def parse_args(self) -> Namespace:
        return self._parser.parse_args()
