from collections.abc import Mapping
from ...namespace import Namespace
from sortedcontainers import SortedList
import uuid
from ...constants import BLUE, WHITE

# column keys
columns = Namespace(
    uuid =        "uuid",
    difficulty =  "difficulty",
    tag =         "tag",
    times =       "times",
    count =       "count"
)

class ProblemStats(Mapping):

    def __init__(self, info=None):
        if info is None:
            info = dict()

        self._info = info
        if columns.uuid not in self._info:
            self._info[columns.uuid] = str(uuid.uuid1())
        if columns.times not in self._info:
            self._info[columns.times] = []
        if columns.count not in self._info:
            self._info[columns.count] = 0

    def _display_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{:d}:{:02d}:{:02d}s'.format(hours, minutes, seconds)

    def display_values(self):
        ''' Table values for display '''
        return [
            self.tag,
            self.count,
            self._display_time(self.median_time()),
            self._display_time(self.best_time()),
            self._display_time(self.worst_time())
        ]

    @staticmethod
    def display_headers():
        ''' Table headers for display '''

        return [columns.tag.capitalize(), columns.count.capitalize(), "Median Time", "Worst Time", "Best Time"]

    @property
    def uuid(self):
        return self._info[columns.uuid]

    @property
    def difficulty(self):
        return self._info[columns.difficulty]

    @difficulty.setter
    def difficulty(self, difficulty):
        self._info[columns.difficulty] = difficulty

    @property
    def tag(self):
        return self._info[columns.tag]

    @tag.setter
    def tag(self, tag):
        self._info[columns.tag] = tag

    @property
    def times(self):
        return self._info[columns.times]

    @property
    def count(self):
        return self._info[columns.count]

    def increment_count(self):
        self._info[columns.count] = self.count + 1

    def median_time(self):
        if not self.times:
            return 0
        sorted_times = SortedList(self.times)
        n = len(sorted_times)

        if n % 2 == 1:
            return sorted_times[n >> 1]
        return (sorted_times[(n - 1) >> 1] + sorted_times[n >> 1]) / 2

    def best_time(self):
        return max(self.times) if self.times else 0

    def worst_time(self):
        return min(self.times) if self.times else 0

    def __getitem__(self, key):
        return self._info[key]

    def __iter__(self):
        return iter(self._info)

    def __len__(self):
        return len(self._info)

    def __str__(self):
        return str(self._info)
