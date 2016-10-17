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

    serve_command = subparsers.add_parser(
        'serve',
        help='Start server that auto-builds on file-change for development'
    )
    serve_command.add_argument(
        '--host',
        type=str,
        default='::1',
        help='IP address to host server on'
    )
    serve_command.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to host server on'
    )

    return parser.parse_args()

def process_args(master_parser):

    parser = master_parser.parser
    print parser
    if parser == 'install':
        Installer('.').install()
        pass

    if parser == 'create':
        Creator('.').create()
        pass

    if parser == 'build':
        Builder('.', 'deploy').build()
        pass

    if parser == 'serve':
        host = master_parser.host
        port = master_parser.port
        Server('.', 'deploy', host=host, port=port).serve()
        pass


def main():
    parser = create_parser()
    process_args(parser)
