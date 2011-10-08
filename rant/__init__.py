from rant.installer import install
from rant.publisher import publish
from rant.generator import generate
import os
try:
    import argparse
except ImportError:
    raise

def main():

    parser = argparse.ArgumentParser(description='Tool to interface with rant. Provides methods to create and edit pages in yaml/markdown, and generate html sites from them.')

    subparsers = parser.add_subparsers(help='sub-command help', dest='parser')

    subparsers.add_parser(
        'install',
        help='Create a new rant project in current directory'
    )

    subparsers.add_parser(
        'publish',
        help='Create a new rant page/post in current directory'
    )

    subparsers.add_parser(
        'generate',
        help='Generate or update static site from all templates and content'
    )

    args = parser.parse_args()

    if args.parser == 'install':
        install(os.getcwd())
        pass

    if args.parser == 'publish':
        publish()
        pass

    if args.parser == 'generate':
        generate()
        pass
