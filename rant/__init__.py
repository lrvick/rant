import argparse

def main():

    parser = argparse.ArgumentParser(description='Tool to interface with rant. Provides methods to create and edit pages in yaml/markdown, and generate html sites from them.')

    parser.add_argument(
        'create',
        action='store',
        help='Create a new rant project in current directory'
    )

    args = parser.parse_args()

    if args.parser == 'create':
        pass
