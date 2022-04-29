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

    def get_vacancies(self, role_id):
        endpoint = 'vacancies'
        params = {'professional_role': role_id}
        vacancies = self.get_json(endpoint=endpoint, params=params)
        return vacancies


if __name__ == '__main__':
    hh_api = HeadHunterApi(base_url=HH_BASE_API_URL, headers=HH_HEADERS)

    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )
    developer_vacancies = hh_api.get_vacancies(role_id=developer_role_id)
