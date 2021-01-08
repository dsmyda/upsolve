from cement import Controller, ex
import webbrowser, time, datetime
from cement import shell
from ..constants import DIFFICULTY_DISPLAY, GREEN, RED

class Next(Controller):

    class Meta:
        label = "next"
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='Get the next problem from the queue'
    )
    def next(self):
        print()
        problem = self.app.problems_table.pop()
        if not problem:
            self.app.log.warning("Nothing to do!\n")
            return

        self.app.log.info("Opening %s%s problem '%s'" % (DIFFICULTY_DISPLAY[problem.difficulty], GREEN, problem.title))
        webbrowser.open(problem.url, new = 2)

        start = time.time()
        p = shell.Prompt("Time started! Press enter once you've solved", default='')
        p.prompt() # Prompt and discard the input.

        end = time.time()
        elapsed = int(end - start)

        minutes, seconds = divmod(elapsed, 60)
        hours, minutes = divmod(minutes, 60)

        self.app.log.info("'%s' took you %s%s\n" % (problem.title, RED,
        '{:d}:{:02d}:{:02d}s'.format(hours, minutes, seconds)))
