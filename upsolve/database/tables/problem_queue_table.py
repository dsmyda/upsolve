from tinydb import where, Query
from ..problem import Problem, CONTEST_CODE, CONTEST_NUMBER, PROBLEM_NUMBER

TABLE_NAME = "problems"

class ProblemQueueTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def add(self, *args):
        ''' Add problems to the table '''

        return self.table.insert_multiple(args)

    def all(self):
        ''' Return all problems in the table '''

        metadata_instances = []
        for raw_json in self.table.all():
            metadata_instances.append(Problem(raw_json))
        return metadata_instances

    def exists(self, contest_code, contest_number, question_number):
        ''' Query if the problem with primary key
            (contest_code, contest_number, question_number) is already present '''

        return self.table.contains(
            (where(CONTEST_CODE) == contest_code) &
            (where(CONTEST_NUMBER) == contest_number) &
            (where(PROBLEM_NUMBER) == question_number)
        )

    def drop(self):
        ''' Drop all problems in the table '''

        self.table.truncate()

    def pop(self):
        ''' Pop off the first problem in the table '''

        if self.size():
            problem = next(iter(self.table))
            self.table.remove(where(UUID) == problem[UUID])
            return Problem(problem)

    def size(self):
        ''' Return the number of problems in the table '''

        return len(self.table)
