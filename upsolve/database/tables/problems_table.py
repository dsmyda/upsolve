from tinydb import where, Query
from ..model.problem import Problem, columns

TABLE_NAME = "problems"

class ProblemsTable:

    def __init__(self, tinydb):
        self.table = tinydb.table(TABLE_NAME)

    def add(self, *problems):
        ''' Add problems to the table '''
        return self.table.insert_multiple(problems)

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
            (where(columns.contest_code) == contest_code) &
            (where(columns.contest_number) == contest_number) &
            (where(columns.problem_number) == question_number)
        )

    def drop(self):
        ''' Drop all problems in the table '''

        self.table.truncate()

    def pop(self):
        ''' Pop off the first problem in the table '''

        if len(self):
            problem = next(iter(self.table))
            self.table.remove(where(columns.uuid) == problem[columns.uuid])
            return Problem(problem)

    def __len__(self):
        ''' Return the number of problems in the table '''

        return len(self.table)
