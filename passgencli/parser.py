import argparse


parser = argparse.ArgumentParser(prog="pass-gen",
                                 description="Strong Passwords Generator with Playfair cypher algorithm")
parser.add_argument("-t", "--text", help="The plain text you want to encode", nargs='+')
parser.add_argument("-k", "--key", help="The key phrase")
parser.add_argument("-v", "--version", help="Show program version", action="version", version='%(prog)s 0.2.0')
args = parser.parse_args()
