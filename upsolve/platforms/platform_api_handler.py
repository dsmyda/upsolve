from .platform_api import PlatformAPI
from cement import Handler
from ..database.problem_metadata import ProblemMetadata

class PlatformAPIHandler(PlatformAPI, Handler):
    '''
    Handler base class to provide a template 'get_metadata' method.
    '''

    def get_metadata(self, contest_number, question_number):
        self.app.log.info("Automatically fetching problem metadata...")
        metadata = self._fetch_metadata(contest_number, question_number)
        return metadata
