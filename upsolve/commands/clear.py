from cement import Controller, ex
from cement import shell

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
        pending_problems = self.app.problems_table.size()
        self.app.log.warning("Dropping %d pending problem(s)." % pending_problems)

        p = shell.Prompt("Are you sure want to continue?", options=[YES_OPTION, NO_OPTION])
        ans = p.prompt()

        if ans == YES_OPTION:
            self.app.problems_table.drop()
            self.app.log.info("Successfully dropped %d problem(s)." \
            " Your queue is now empty.\n" % pending_problems)
        else:
            self.app.log.info("Operation aborted.\n")
