TABLE_NAME = "stats"

class ProblemStatsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def record_time(self, problem, duration):
        pass
