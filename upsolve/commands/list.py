from cement import Controller, ex
from ..database.model.problem import Problem

class List(Controller):

    class Meta:
        label = 'list'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='List all problems in the queue'
    )
    def list(self):
        print()
        headers = Problem.display_headers()
        problems = self.app.problems_service.list()
        values = [problem.display_values() for problem in problems]
        self.app.render(values, headers=headers)
