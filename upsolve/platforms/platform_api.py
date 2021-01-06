from abc import abstractmethod
from cement import Interface

class PlatformAPI(Interface):
    ''' The necessary APIs to implement in order to support
        a new platform '''

    class Meta:
        interface = "platform_api"

    @abstractmethod
    def get_metadata(self, contest_number, question_number):
        '''
        Get problem metadata from the contest using the contest number
        and question number.
        '''
        pass
