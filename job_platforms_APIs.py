import urllib.parse as urllib

import requests


class BaseApi:
    """Base API class which implements with all repeatable attributes and methods."""

    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_json(self, endpoint: str, params: dict = None) -> dict:
        """Make full url and send GET request.
        :param endpoint: - it is a point to interact with definite method to API.
        :param params: - additional data for getting info from response.
        :returns: response.json() - information from response in dict data structure.
        """
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()


class SuperJob(BaseApi):
    """Class to interact with SuperJob API. Inherited from BaseApi"""

    def get_authorize(self, client_id: int, url: str):
        """Get code for getting access token.
        :param client_id: - Application ID registered in the API.
        :param url: - Url for user authorization request.
        """
        params = {
            'client_id': client_id,
            'redirect_uri': 'https://api.superjob.ru',
        }
        response = self.session.get(url=url, params=params)
        response.raise_for_status()

    def get_access_token(self, client_id: int, secret_key: str, code: str) -> str:
        """Get access token for authorized requests.
        :param client_id: - Application ID registered in the API.
        :param secret_key: - SuperJob's API client secret key.
        :param code: - Code, received in case of successful user authorization.
        :returns: access_token - Access_token. It must be passed to all methods that require authentication.
        """
        endpoint = 'oauth2/access_token/'
        params = {
            'client_id': client_id,
            'client_secret': secret_key,
            'redirect_uri': 'https://api.superjob.ru',
            'code': code,
        }
        access_token = self.get_json(endpoint=endpoint, params=params)['access_token']
        return access_token

    def get_vacancies(self, params: dict) -> list:
        """Get vacancies from SuperJob platform.
        :param params: - Necessary information for getting data.
        :returns: vacancies - Vacancies with all useful data about them.
        """
        endpoint = 'vacancies'
        vacancies = self.get_json(endpoint=endpoint, params=params)
        return vacancies['objects']


class HeadHunterApi(BaseApi):
    """Class to interact with HeadHunter API. Inherited from BaseApi"""

    def get_professional_roles(self) -> list:
        """Get professional roles in order to get developer role id."""
        endpoint = 'professional_roles'
        professional_roles = self.get_json(endpoint=endpoint)
        return professional_roles['categories']

    def get_vacancies(self, params: dict, page: int = None) -> dict:
        """Get vacancies with certain page.
        :param params: - Necessary information for getting data.
        :param page: - SuperJob's API client secret key.
        :returns: vacancies - Vacancies with all useful data at certain page.
        """
        endpoint = 'vacancies'
        params.update({'page': page})
        vacancies = self.get_json(endpoint=endpoint, params=params)
        return vacancies

    def get_all_vacancies(self, params: dict) -> list:
        """Get vacancies from all pages.
        :param params: - Necessary information for getting data.
        :returns: all_vacancies - Vacancies from all pages.
        """
        all_vacancies = []
        vacancies = self.get_vacancies(params)
        page, pages = vacancies['page'], vacancies['pages']

        while page < pages:
            vacancies = self.get_vacancies(params, page=page)
            all_vacancies.extend(vacancies['items'])
            page += 1

        return all_vacancies

    @staticmethod
    def get_role_id(query_industry: str, query_job: str, roles: list) -> int:
        """Get role id of a vacancy.
        :param query_industry: - Certain industry of work that we search for.
        :param query_job: - Certain job that we search for.
        :param roles: - All industries from a job platform.
        :returns: role_id - ID of the role that we search for.
        """
        industry_jobs = None

        for role in roles:
            if query_industry in role['name']:
                industry_jobs = role['roles']
                break

        for industry_job in industry_jobs:
            if query_job in industry_job['name']:
                role_id = industry_job['id']
                return role_id
