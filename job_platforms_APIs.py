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
        :param endpoint: - it is a point to interact with definite method to API
        :param params: - additional data for getting info from response
        :returns: response.json() - information from response in dict data structure
        """
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()


class HeadHunterApi(BaseApi):

    def get_professional_roles(self):
        endpoint = 'professional_roles'
        professional_roles = self.get_json(endpoint=endpoint)
        return professional_roles['categories']

    def get_role_id(self, query_industry, query_job, roles):
        industry_jobs = None

        for role in roles:
            if query_industry in role['name']:
                industry_jobs = role['roles']

        for industry_job in industry_jobs:
            if query_job in industry_job['name']:
                role_id = industry_job['id']
                return role_id

    def get_vacancies(self, role_id, area_id, period):
        endpoint = 'vacancies'
        params = {
            'professional_role': role_id,
            'area': area_id,
            'period': period,
        }
        vacancies = self.get_json(endpoint=endpoint, params=params)
        return vacancies
