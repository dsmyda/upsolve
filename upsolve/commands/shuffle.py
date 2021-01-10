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
        problems = self.app.problems_service.list()
        random.shuffle(problems)
        self.app.problems_service.delete_all()
        self.app.problems_service.save(*problems)
        log.info("Shuffled %d problems" % len(problems))
        log.info("You can view the new queue by running %s'upsolve list'\n" % WHITE)
