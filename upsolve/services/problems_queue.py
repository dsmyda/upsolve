from tinydb import where, Query
from ..database.model.problem import Problem, columns

class ProblemsQueue:

    def __init__(self, tinydb, metrics_service):
        self.queue_table = tinydb.table("queue")
        self.metrics_service = metrics_service

    def save(self, *problems):
        ''' Add problems to the table '''
        ret = self.queue_table.insert_multiple(problems)
        self.metrics_service.notify(*problems)
        return ret

    def list(self):
        ''' Return all problems in the table '''

        metadata_instances = []
        for raw_json in self.queue_table.all():
            metadata_instances.append(Problem(raw_json))
        return metadata_instances

    def exists(self, contest_code, contest_number, question_number):
        ''' Query if the problem with primary key
            (contest_code, contest_number, question_number) is already present '''

        return self.queue_table.contains(
            (where(columns.contest_code) == contest_code) &
            (where(columns.contest_number) == contest_number) &
            (where(columns.problem_number) == question_number)
        )

    def delete_all(self):
        ''' Drop all problems in the table '''

        self.queue_table.truncate()

    def next_problem(self):
        ''' Pop off the first problem in the table '''

        if self.count():
            problem = next(iter(self.queue_table))
            self.queue_table.remove(where(columns.uuid) == problem[columns.uuid])
            return Problem(problem)

    def count(self):
        ''' Return the number of problems in the table '''

        return len(self.queue_table)
