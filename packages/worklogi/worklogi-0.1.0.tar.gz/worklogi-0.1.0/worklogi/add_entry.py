from argparse import ArgumentParser, Namespace
from datetime import datetime

from .database import WorkLogDatabase

from .entry import Entry


def configure_add_entry_parser(parser: ArgumentParser):
    parser.add_argument('branch', type=str)

def add_entry(args: Namespace):
    commit_string = input("Enter commit title: ")

    now = datetime.now().timestamp()
    entry = Entry(title=commit_string, timestamp=int(now), branch=args.branch)

    WorkLogDatabase.save_entry(entry)
