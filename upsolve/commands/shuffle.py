from cement import Controller, ex
import random

class Shuffle(Controller):

    class Meta:
        label = "shuffle"
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='Shuffle problems in the queue'
    )
    def shuffle(self):
        print()
        problems = self.app.problems_table.all()
        random.shuffle(problems)
        self.app.problems_table.drop()
        self.app.problems_table.add(*problems)
        self.app.log.info("Shuffled %d problems\n" % len(problems))
