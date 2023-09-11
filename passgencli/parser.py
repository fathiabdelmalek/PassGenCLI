from argparse import ArgumentParser, Namespace


class Parser:
    def __init__(self):
        self._parser = ArgumentParser(prog="pass-gen",
                                      description="Strong passwords generator with Playfair cypher algorithm")
        self._parser.add_argument("-v", "--version", action="version", version='%(prog)s 0.6.0',
                                  help="Print version information and exit")

        sp = self._parser.add_subparsers(title="Subcommands", dest="command",
                                         description="Choose a command to generate passwords or configure settings.")

        generate_parser = sp.add_parser("generate", help="Generate passwords from text and key")
        generate_parser.add_argument("-t", "--text", nargs='+', help="The plain text you want to encode")
        generate_parser.add_argument("-k", "--key", help="The key phrase")
        generate_parser.epilog = "Example: pass-gen generate -t 'my text' -k 'my_key'"

        config_parser = sp.add_parser("config", help="Configure settings")
        config_parser.add_argument("--replace", nargs=2, metavar=('character', 'replacement'),
                                   help="Replace one character with a set of characters after cipher")
        config_parser.add_argument("--reset", nargs=1, metavar='character',
                                   help="Reset a character to it's default value")
        config_parser.add_argument("--clear", action='store_true', help="Clear the history")
        config_parser.epilog = (
            "Examples:\n"
            "1. Replace a character: pass-gen config --replace e '1@2#'\n"
            "2. Reset a character: pass-gen config --reset a\n"
            "3. Clear history: pass-gen config --clear"
        )

    def parse_args(self) -> Namespace:
        return self._parser.parse_args()
