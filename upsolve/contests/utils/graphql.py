from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

class GraphQL:

    @staticmethod
    def execute(endpoint, query, variables = {}):
        synchronous_http_transport = RequestsHTTPTransport(
            url=endpoint, verify=True, retries=3
        )
        client = Client(transport=synchronous_http_transport)
        return client.execute(gql(query), variable_values=variables)
