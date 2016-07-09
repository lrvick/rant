from rant.init import Initializer
from rant.create import Creator
from rant.build import Builder
try:
    from argparse import ArgumentParser
except ImportError:
    raise


def main():

    parser = ArgumentParser(description="""
        Tool to interface with rant. Provides methods to create and edit pages
        in yaml/markdown, and generate html sites from them.
    """)

    subparsers = parser.add_subparsers(help='sub-command help', dest='parser')

    subparsers.add_parser(
        'init',
        help='initialize a new rant project in current directory'
    )

    subparsers.add_parser(
        'create',
        help='Create a new rant page/post in current directory'
    )

    subparsers.add_parser(
        'build',
        help='Build static site from your source templates and content'
    )

    args = parser.parse_args()

    if args.parser == 'init':
        initializer = Initializer('.')
        initializer.init()
        pass

    if args.parser == 'create':
        creator = Creator('.')
        creator.create()
        pass

    if args.parser == 'build':
        builder = Builder('.', 'deploy')
        builder.build()
        pass
