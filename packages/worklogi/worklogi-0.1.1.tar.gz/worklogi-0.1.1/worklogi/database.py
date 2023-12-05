from os.path import expanduser
from pathlib import Path
from dataclasses import asdict
from json import dumps, loads
from typing import Any, Generator 

from .entry import Entry

class WorkLogDatabase:
    WORKLOG_DB_LOCATION = expanduser("~/.local/worklog.db")

    @classmethod
    def ensure_file_is_created(cls):
        Path(cls.WORKLOG_DB_LOCATION).touch()

    @classmethod
    def save_entry(cls, entry: Entry):
        with open(cls.WORKLOG_DB_LOCATION, 'a') as f:
            entry_dict = asdict(entry)
            entry_json = dumps(entry_dict)
            f.write(entry_json)
            f.write("\n")
    
    @classmethod
    def get_entries(cls) -> Generator[Entry, Any, Any]:
        with open(cls.WORKLOG_DB_LOCATION, 'r') as f:
            for line in f:
                entry_json = loads(line)
                entry = Entry(**entry_json)
                yield entry


WorkLogDatabase.ensure_file_is_created()
