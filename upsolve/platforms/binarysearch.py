from .platform_api_handler import PlatformAPIHandler

CONTEST_URL_TEMPLATE = ""

class BinarySearch(PlatformAPIHandler):

    class Meta:
        label = "binarysearch"

    def _fetch_metadata(self, contest_number, question_number):
        self.app.log.info("Querying binarysearch for metadata...")
        # TODO query the binary search API
