import urllib.parse as urllib

import requests

from apis_constants import HH_HEADERS, HH_BASE_API_URL


class BaseApi:
    """Base API class which implements with all repeatable attributes and methods."""

    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_json(self, endpoint: str, params: dict = None) -> dict:
        """Make full url and send GET request.
        :param endpoint: - it is a point to interact with definite method to API
        :param params: - additional data for getting info from response
        :returns: response.json() - information from response in dict data structure
        """
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()


class HeadHunterApi(BaseApi):

    def get_authorization_code(self):
        endpoint = 'oauth/authorize'
        url = f'https://hh.ru/{endpoint}'
        params = {
            'response_type': 'code',
            'client_id': 83918056,
        }
        authorization_code = self.session.post(url=url, params=params)

    def get_access_token(self, client_id: str, client_secret: str):
        endpoint = 'oauth/token'
        url = f'https://hh.ru/{endpoint}'
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
        }
        access_token = self.session.post(url=url, params=params)
        access_token.raise_for_status()
        return access_token

    def get_vacancies(self, query):
        endpoint = f'vacancies/{query}'
        vacancies = self.get_json(endpoint=endpoint)
        return vacancies


if __name__ == '__main__':
    hh_api = HeadHunterApi(base_url=HH_BASE_API_URL, headers=HH_HEADERS)
    developer_vacancies = hh_api.get_authorization_code()
