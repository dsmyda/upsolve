from cement import Controller, ex
from ..constants import WHITE
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
        log = self.app.log
        problems = self.app.problems_queue.list()
        random.shuffle(problems)
        self.app.problems_queue.delete_all()
        self.app.problems_queue.save(*problems)
        log.info("Shuffled %d problems" % len(problems))
        log.info("You can view the new queue by running %s'upsolve list'\n" % WHITE)
