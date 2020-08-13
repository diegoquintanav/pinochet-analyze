from datetime import datetime
import typing as T
import hashlib


class Neo4jDatePair:
    def __init__(self, value, format):
        self.value = value
        self.format = format

    def to_datetime(self):
        return datetime(self.value, self.format)


def to_md5(elements: T.List, *args, **kwargs) -> str:
    pre = "".join(str(arg).lower() for arg in elements)
    return hashlib.md5(pre.encode("utf-8")).hexdigest()

def to_isoformat(datestring: str) -> str:
    return datetime.strptime(datestring, "%Y-%m-%d").date().isoformat()