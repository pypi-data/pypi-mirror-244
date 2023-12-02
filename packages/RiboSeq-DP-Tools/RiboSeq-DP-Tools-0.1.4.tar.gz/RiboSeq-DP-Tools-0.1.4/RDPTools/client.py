
import requests

class RDPClient:
    def __init__(self, base_url="https://rdp.ucc.ie/api", auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token

    def make_api_request(self, endpoint, params=None):
        headers = {
            'Authorization': f'Token {self.auth_token}',
            'Accept': 'application/json'
        } if self.auth_token else {
            'Accept': 'application/json'
        }

        response = requests.get(f'{self.base_url}/{endpoint}', params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def list_sample_fields(self):
        return self.make_api_request('samples/fields/')

    def query_samples(self, query, fields=None, limit=100):
        params = {'query': query, 'fields': fields, 'limit': limit}
        return self.make_api_request('samples', params=params)