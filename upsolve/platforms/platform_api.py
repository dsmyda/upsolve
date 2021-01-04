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
        Get problem info from the contest using the contest number
        and question number. Each platform specific class should
        override _fetch_problem_info and call their respective APIs.
        This method is templated in PlatformHandler.
        '''
        pass

    @abstractmethod
    def _fetch_metadata(self, contest_number, question_number):
        pass
