from rant.install import Installer
from rant.create import Creator
from rant.build import Builder
from rant.serve import Server
from argparse import ArgumentParser


def create_parser():

    parser = ArgumentParser(description="""
        Tool to interface with rant. Provides methods to create and edit pages
        in yaml/markdown, and generate html sites from them.
    """)

    subparsers = parser.add_subparsers(help='sub-command help', dest='parser')

    subparsers.add_parser(
        'install',
        help='Install a new rant project in current directory'
    )

    subparsers.add_parser(
        'create',
        help='Create a new rant page/post in current directory'
    )

    subparsers.add_parser(
        'build',
        help='Build static site from your source templates and content'
    )

    subparsers.add_parser(
        'serve',
        help='Start server that auto-builds on file-change for development'
    )

    return parser


def process_args(args):

    if args.parser == 'install':
        Installer('.').install()
        pass

    if args.parser == 'create':
        Creator('.').create()
        pass

    if args.parser == 'build':
        Builder('.', 'deploy').build()
        pass

    if args.parser == 'serve':
        Server('.', 'deploy').serve()
        pass


def main():
    parser = create_parser()
    args = parser.parse_args()
    process_args(args)
