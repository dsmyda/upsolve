from collections.abc import Mapping
from ...namespace import Namespace
import uuid

# column keys
columns = Namespace(
    uuid =        "uuid",
    tag =         "tag",
    count =       "count"
)

class TagMetrics(Mapping):

    def __init__(self, info=None):
        self._info = {} if not info else info
        if columns.uuid not in self._info:
            self._info[columns.uuid] = str(uuid.uuid1())
        if columns.count not in self._info:
            self._info[columns.count] = 0

    def display_values(self):
        ''' Table values for display '''
        return [
            self.tag,
            self.count
        ]

    @staticmethod
    def headers():
        ''' Table headers for display '''

        return [columns.tag.capitalize(), columns.count.capitalize()]

    @property
    def uuid(self):
        return self._info[columns.uuid]

    @property
    def tag(self):
        return self._info[columns.tag]

    @tag.setter
    def tag(self, tag):
        self._info[columns.tag] = tag

    @property
    def count(self):
        return self._info[columns.count]

    def increment_count(self):
        self._info[columns.count] = self.count + 1

    def __getitem__(self, key):
        return self._info[key]

    def __iter__(self):
        return iter(self._info)

    def __len__(self):
        return len(self._info)

    def __str__(self):
        return str(self._info)
