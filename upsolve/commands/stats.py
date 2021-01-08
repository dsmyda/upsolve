from cement import Controller, ex

class Stats(Controller):

    class Meta:
        label = 'stats'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='List stats'
    )
    def stats(self):
        pass
