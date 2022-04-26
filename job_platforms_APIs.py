import requests


class BaseApi:
    """Base API class which implements with all repeatable attributes and methods."""

    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)


class HeadHunterApi(BaseApi):

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


if __name__ == '__main__':
    hh_api = HeadHunterApi(base_url='https://api.hh.ru/', headers={})
    access_token = hh_api.get_access_token(client_id=client_id, client_secret=client_secret)
