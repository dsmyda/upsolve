from cement import Controller, ex
from cement import shell
from ..constants import WHITE

YES_OPTION, NO_OPTION = "y", "n"

class Clear(Controller):

    class Meta:
        label = 'clear'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='Clear all questions in the queue'
    )
    def clear(self):
        print()
        log = self.app.log
        pending_problems = self.app.problems_service.size()
        log.warning("Dropping %d pending problem(s)." % pending_problems)

        p = shell.Prompt("Are you sure want to continue?", options=[YES_OPTION, NO_OPTION])
        ans = p.prompt()

        if ans == YES_OPTION:
            self.app.problems_service.delete_all()
            print()
            log.info("Successfully dropped %d problem(s)." \
            " Your queue is now empty" % pending_problems)
            log.info("You can add new problems by running %s'upsolve contest'\n" % WHITE)
        else:
            self.app.log.info("Operation aborted.\n")
