from tinydb import where, Query

TABLE_NAME = "stats"

class ProblemStatsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def record_time(self, problem, duration):
        # Use problem tag, difficulty to index duration
        pass

    def all(self, difficulty):
        return []
