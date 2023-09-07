from argparse import ArgumentParser


parser = ArgumentParser(prog="pass-gen", description="Strong passwords generator with Playfair cypher algorithm")
parser.add_argument("-v", "--version", help="Print version information and exit", action="version",
                    version='%(prog)s 0.3.0')

subparsers = parser.add_subparsers(title="Subcommands", dest="command", required=True,
                                   description="Choose a command to generate passwords or configure settings.")

generate_parser = subparsers.add_parser("generate", help="Generate passwords from text and key")
generate_parser.add_argument("-t", "--text", help="The plain text you want to encode", nargs='+')
generate_parser.add_argument("-k", "--key", help="The key phrase")
generate_parser.epilog = "Example: pass-gen generate -t 'mytext' -k 'mykey'"

config_parser = subparsers.add_parser("config", help="Configure settings")
config_parser.add_argument("--replace",
                           help="Replace one character with a set of characters after cipher", nargs=2,
                           metavar=('character', 'replacement'))
config_parser.add_argument("--reset", help="Reset a character to it's default value", nargs=1,
                           metavar='character')
config_parser.epilog = (
    "Examples:\n"
    "1. Replace a character: pass-gen config --replace e '1@2#'\n"
    "2. Reset a character: pass-gen config --reset a"
)
args = parser.parse_args()
