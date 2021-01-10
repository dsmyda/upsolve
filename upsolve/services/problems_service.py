from tinydb import where, Query
from ..database.model.problem import Problem, columns

class ProblemsService:

    def __init__(self, tinydb, stats_service):
        self.table = tinydb.table("problems")
        self.stats_service = stats_service

    def save(self, *problems):
        ''' Add problems to the table '''
        ret = self.table.insert_multiple(problems)
        self.stats_service.update_counts(*problems)
        return ret

    def list(self):
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

    def delete_all(self):
        ''' Drop all problems in the table '''

        self.table.truncate()

    def next_problem(self):
        ''' Pop off the first problem in the table '''

        if self.count():
            problem = next(iter(self.table))
            self.table.remove(where(columns.uuid) == problem[columns.uuid])
            return Problem(problem)

    def count(self):
        ''' Return the number of problems in the table '''

        return len(self.table)
