import urllib.parse as urllib

import requests

from analyzer_tools import predict_salary


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


class SuperJob(BaseApi):
    """Class to interact with SuperJob API. Inherited from BaseApi"""

    def get_authorize(self, client_id: int, url: str):
        """Get code for getting access token.
        :param client_id: - Application ID registered in the API
        :param url: - Url for user authorization request
        """
        params = {
            'client_id': client_id,
            'redirect_uri': 'https://api.superjob.ru',
        }
        response = self.session.get(url=url, params=params)
        response.raise_for_status()

    def get_access_token(self, client_id: int, secret_key: str, code: str) -> str:
        """Get access token for authorized requests.
        :param client_id: - Application ID registered in the API
        :param secret_key: - SuperJob's API client secret key
        :param code: - Code, received in case of successful user authorization
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

    @staticmethod
    def predict_rub_salary(vacancies):
        expected_salaries = []

        for vacancy in vacancies:
            currency = vacancy['currency']
            start_salary = vacancy['payment_from']
            end_salary = vacancy['payment_to']
            currency_name = 'rub'

            expected_salary = predict_salary(
                currency=currency, start_salary=start_salary,
                end_salary=end_salary, currency_name=currency_name
            )
            if expected_salary:
                expected_salaries.append(expected_salary)
        return expected_salaries


class HeadHunterApi(BaseApi):

    def get_professional_roles(self):
        endpoint = 'professional_roles'
        professional_roles = self.get_json(endpoint=endpoint)
        return professional_roles['categories']

    def get_vacancies(self, params, page=None):
        endpoint = 'vacancies'
        params.update({'page': page})
        vacancies = self.get_json(endpoint=endpoint, params=params)
        return vacancies

    def get_all_vacancies(self, params):
        all_vacancies = []
        page, pages = self.get_number_pages(params)

        while page < pages:
            vacancies = self.get_vacancies(params, page=page)
            all_vacancies.extend(vacancies['items'])
            page += 1
        return all_vacancies

    def get_number_pages(self, params):
        vacancies = self.get_vacancies(params)
        return vacancies['page'], vacancies['pages']

    @staticmethod
    def predict_rub_salary(vacancies):
        expected_salaries = []

        for vacancy in vacancies:
            salary = vacancy['salary']

            if not salary:
                continue

            currency = salary['currency']
            start_salary = salary['from']
            end_salary = salary['to']
            currency_name = 'RUR'

            expected_salary = predict_salary(
                currency=currency, start_salary=start_salary,
                end_salary=end_salary, currency_name=currency_name
            )
            if expected_salary:
                expected_salaries.append(expected_salary)

        return expected_salaries

    @staticmethod
    def get_role_id(query_industry, query_job, roles):
        industry_jobs = None

        for role in roles:
            if query_industry in role['name']:
                industry_jobs = role['roles']

        for industry_job in industry_jobs:
            if query_job in industry_job['name']:
                role_id = industry_job['id']
                return role_id
