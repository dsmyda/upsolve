from abc import abstractmethod
from cement import Interface

class ContestInterface(Interface):
    ''' The necessary APIs to implement in order to support
        a new platform's contest '''

    class Meta:
        interface = "contest_api"

    @abstractmethod
    def get_metadata(self, contest_number, question_number):
        '''
        Get problem metadata from the contest using the contest number
        and question number.
        '''
        pass

    @abstractmethod
    def get_questions_metadata(self, contest_number):
        '''
        Get all problem metadata from the contest.
        '''
        pass
