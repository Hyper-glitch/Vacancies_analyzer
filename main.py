import os

from dotenv import load_dotenv

from analyzer_tools import get_analyzed_vacancies
from job_platforms_APIs import HeadHunterApi, SuperJob


def run_head_hunter_analyzer(programming_languages: list, hh_app_name: str, hh_app_email: str):
    headers = {'User-Agent': f'{hh_app_name}-{hh_app_email}'}
    base_url = 'https://api.hh.ru/'
    area_id = 2  # todo add location resolver
    period = 30
    per_page = 100

    hh_api = HeadHunterApi(base_url=base_url, headers=headers)

    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )
    params = {
        'professional_role': developer_role_id,
        'area': area_id,
        'period': period,
        'per_page': per_page,
    }
    analyzed_vacancies = get_analyzed_vacancies(
        api=hh_api, search_key='text',
        programming_languages=programming_languages,
        vacancies_params=params,
    )
    print(analyzed_vacancies)


def run_super_job_analyzer(programming_languages, client_id, secret_key, code):
    headers = {'X-Api-App-Id': secret_key}
    base_url = 'https://api.superjob.ru/2.0/'
    auth_url = 'https://www.superjob.ru/authorize/'
    town = 'Санкт-Петербург'
    catalogues = 33
    params = {
        'client_id': client_id,
        'secret_key': secret_key,
        'catalogues': catalogues,
        'town': town,
    }

    sj_api = SuperJob(base_url=base_url, headers=headers)
    if not code:
        sj_api.get_authorize(client_id=client_id, url=auth_url)
        access_token = sj_api.get_access_token(client_id=client_id, secret_key=secret_key, code=code)

    analyzed_language_vacancies = get_analyzed_vacancies(
        api=sj_api, search_key='keyword',
        programming_languages=programming_languages,
        vacancies_params=params,
    )
    print(analyzed_language_vacancies)


def main():
    """The main logic for running the whole program."""
    load_dotenv()

    hh_app_name = os.environ.get("HH_APP_NAME")
    hh_app_email = os.environ.get("HH_APP_EMAIL")
    sj_client_id = int(os.environ.get("SUPER_JOB_CLIENT_ID"))
    sj_secret_key = os.environ.get("SUPER_JOB_SECRET_KEY")
    sj_code = os.environ.get("CODE")
    programming_languages = ['JavaScript', 'C#', 'Java',
                             'Python', 'PHP', 'TypeScript',
                             'Kotlin', 'Swift', 'C++', 'Go']

    run_head_hunter_analyzer(
        programming_languages=programming_languages, hh_app_name=hh_app_name, hh_app_email=hh_app_email,
    )
    run_super_job_analyzer(
        programming_languages=programming_languages, client_id=sj_client_id, secret_key=sj_secret_key, code=sj_code,
    )


if __name__ == '__main__':
    main()
