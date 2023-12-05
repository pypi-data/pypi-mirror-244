from dataclasses import dataclass
from datetime import datetime

@dataclass
class Entry:
    timestamp: int 
    title: str
    branch: str

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

    @classmethod
    def get_header(cls):
        return ['TIME', 'BRANCH', 'TITLE']

    def __str__(self) -> str:
        time = self.datetime()
        return "\t".join([time.isoformat(), self.branch, self.title])

    def get_data(self):
        time = self.datetime()
        return [time.isoformat(), self.branch, self.title]
