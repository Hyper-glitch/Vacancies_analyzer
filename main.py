import os

from dotenv import load_dotenv

from analyzer_tools import get_statistics, show_statistics
from api_job_platforms import HeadHunter, SuperJob


def analyze_head_hunter(programming_languages: list, hh_app_name: str, hh_app_email: str):
    """Initialize api and run methods for getting and analyzing HeadHunter vacancies."""

    headers = {'User-Agent': f'{hh_app_name}-{hh_app_email}'}
    base_url = 'https://api.hh.ru/'
    title = 'HeadHunter Санкт-Петербург'

    hh_api = HeadHunter(base_url=base_url, headers=headers)

    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )
    vacancies_params = {
        'professional_role': developer_role_id,
        'area': 2,
        'period': 30,
        'per_page': 100,
    }
    statistics = get_statistics(
        api=hh_api, search_key='text', programming_languages=programming_languages,
        vacancies_params=vacancies_params,
    )
    show_statistics(statistics=statistics, title=title)


def analyze_super_job(programming_languages, client_id, secret_key, code):
    """Initialize api and run methods for getting and analyzing SuperJob vacancies."""

    headers = {'X-Api-App-Id': secret_key}
    base_url = 'https://api.superjob.ru/2.0/'
    auth_url = 'https://www.superjob.ru/authorize/'
    town = 'Санкт-Петербург'
    title = f'SuperJob {town}'
    catalogues = 33
    vacancies_params = {
        'client_id': client_id,
        'secret_key': secret_key,
        'catalogues': catalogues,
        'town': town,
    }

    sj_api = SuperJob(base_url=base_url, headers=headers)

    if not code:
        sj_api.get_authorize(client_id=client_id, url=auth_url)
        access_token = sj_api.get_access_token(client_id=client_id, secret_key=secret_key, code=code)

    statistics = get_statistics(
        api=sj_api, search_key='keyword', programming_languages=programming_languages,
        vacancies_params=vacancies_params,
    )
    show_statistics(statistics=statistics, title=title)


def vacancies_analyzer():
    """The main logic for running the whole program."""
    load_dotenv()

    hh_app_name = os.environ.get("HH_APP_NAME")
    hh_app_email = os.environ.get("HH_APP_EMAIL")
    sj_client_id = int(os.environ.get("SUPER_JOB_CLIENT_ID"))
    sj_secret_key = os.environ.get("SUPER_JOB_SECRET_KEY")
    sj_code = os.environ.get("CODE")

    programming_languages = [
        'JavaScript', 'C#', 'Java',
        'Python', 'PHP', 'TypeScript',
        'Kotlin', 'Swift', 'C++', 'Go',
    ]

    analyze_head_hunter(
        programming_languages=programming_languages, hh_app_name=hh_app_name, hh_app_email=hh_app_email,
    )
    analyze_super_job(
        programming_languages=programming_languages, client_id=sj_client_id, secret_key=sj_secret_key, code=sj_code,
    )


if __name__ == '__main__':
    vacancies_analyzer()
