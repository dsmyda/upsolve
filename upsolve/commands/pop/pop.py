from cement import Controller, ex
import webbrowser, time, datetime
from cement import shell

class Pop(Controller):
    class Meta:
        label = "pop"
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='pop a contest question'
    )
    def pop(self):
        problem = self.app.problems_table.pop()
        if not problem:
            self.app.log.warning("Nothing to do!\n")
            return

        self.app.log.info("Starting problem '%s'" % problem.title)
        webbrowser.open(problem.url, new = 2)

        start = time.time()
        p = shell.Prompt("Time started! Press enter once you've solved", default='')
        p.prompt() # Prompt and discard the input.

        end = time.time()
        elapsed = int(end - start)

        minutes, seconds = divmod(elapsed, 60)
        hours, minutes = divmod(minutes, 60)

        self.app.log.info("%s took you %s" % (problem.title,
        '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)))
