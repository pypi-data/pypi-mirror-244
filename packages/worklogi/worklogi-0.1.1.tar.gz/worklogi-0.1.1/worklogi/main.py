from argparse import ArgumentParser

from .browse_entries import browse_entries

from .add_entry import configure_add_entry_parser, add_entry

commands = {
    'add-entry': add_entry,
    'browse': browse_entries
}

def main():
    parser = ArgumentParser('worklogi')
    subparsers = parser.add_subparsers(title="Action", required=True, dest='command')

    add_entry_parser = subparsers.add_parser('add-entry')
    configure_add_entry_parser(add_entry_parser)

    subparsers.add_parser('browse')

    args = parser.parse_args()
    commands[args.command](args)


