from cement import Controller, ex
import random
from ..view.view import View

class Shuffle(Controller):
    class Meta:
        label = "shuffle"
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='shuffle the question queue'
    )
    def shuffle(self):
        problems = self.app.problems_table.all()
        random.shuffle(problems)
        self.app.problems_table.delete_all()
        self.app.problems_table.add(*problems)
        self.app.log.info("Shuffled %d problems\n" % len(problems))
