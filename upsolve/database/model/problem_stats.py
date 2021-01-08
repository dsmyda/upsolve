from collections.abc import Mapping
from ..namespace import Namespace
import uuid

# column keys
columns = Namespace(
    uuid =        "uuid",
    difficulty =  "difficulty",
    tag =         "tag",
    median_time = "median_time",
    best_time =   "best_time",
    worst_time =  "worst_time"
)

class ProblemStats(Mapping):

    def __init__(self, info=None):
        if info is None:
            info = dict()
            
        self._info = info
        if columns.uuid not in self._info:
            self._info[columns.uuid] = str(uuid.uuid1())

    def values(self):
        ''' Table values for display '''
        pass
        #return [
        #    self.tag,
        #    self.median_time,
        #    self.best_time,
        #    self.worst_time
        #]

    @staticmethod
    def headers():
        ''' Table headers for display '''

        return [columns.tag, columns.median_time, columns.best_time, columns.worst_time]
