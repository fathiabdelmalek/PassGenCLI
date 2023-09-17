from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter, RawTextHelpFormatter


class Parser:
    def __init__(self, version):
        self._parser = ArgumentParser(prog="pass-gen",
                                      description="Strong passwords generator with Playfair cypher algorithm")
        self._parser.epilog = "Run pass-gen <command> --help for more information on a command."
        self._parser.add_argument("-v", "--version", action="version", version=f'%(prog)s {version}',
                                  help="Print version information and exit")
        sp = self._parser.add_subparsers(title="Commands", dest="command")
        # generate password parser
        generate_parser = sp.add_parser("generate", help="Generate passwords from text and key",
                                        description="Generate passwords from text and key")
        generate_parser.add_argument("-t", "--text", nargs='+', help="The plain text you want to encode")
        generate_parser.add_argument("-k", "--key", help="The key phrase")
        generate_parser.add_argument("-c", "--context", nargs='+',
                                     help="The context if you want to save the password on history")
        generate_parser.epilog = "Example: pass-gen generate -t 'my text' -k 'my_key' -c 'my context'"
        # get password parser
        get_password_parser = sp.add_parser("get", help="Retrieve a saved password by it's context",
                                            description="Retrieve a saved password by it's context")
        get_password_parser.add_argument("context", nargs='+', help="The context of the saved password")
        get_password_parser.epilog = "Example: pass-gen get 'my context'"
        # remove password parser
        remove_password_parser = sp.add_parser("remove", help="Remove save password from history",
                                               description="Remove save password from history")
        remove_password_parser.add_argument("context", nargs='+', help="The context of the saved password")
        remove_password_parser.epilog = "Example: pass-gen remove 'my context'"
        # replace character parser
        replace_character_parser = sp.add_parser("replace",
                                                 help="Replace one character with a set of characters after cipher",
                                                 description="Replace one character with a set of characters after cipher")
        replace_character_parser.add_argument("character",
                                              help="Character to be replaced (should be one character)")
        replace_character_parser.add_argument("replacement", nargs=1,
                                              help="The replacement string (should not contain spaces)")
        replace_character_parser.epilog = "Example: pass-gen replace e '1@2#"
        # reset character parser
        reset_character_parser = sp.add_parser("reset", help="Reset a character to it's default value",
                                               description="Reset a character to it's default value")
        reset_character_parser.add_argument("character", nargs=1, help="Character to reset it")
        reset_character_parser.epilog = "Example: pass-gen reset e"
        sp.add_parser("clear", help="Clear the history", description="Clear the history")  # clear history parser

    def parse_args(self) -> Namespace:
        return self._parser.parse_args()
