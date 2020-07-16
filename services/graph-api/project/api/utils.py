from datetime import datetime


class Neo4jDatePair:
    def __init__(self, value, format):
        self.value = value
        self.format = format

    def to_datetime(self):
        return datetime(self.value, self.format)
