import argparse


parser = argparse.ArgumentParser(description="Strong Passwords Generator made with Python")
parser.add_argument("-t", "--text", nargs='+', help="The plain text you want to encode")
parser.add_argument("-k", "--key", help="The key phrase")
parser.add_argument("-m", "--matrix", action="store_true", help="Show the used matrix in the encryption")
args = parser.parse_args()
