import os

from dotenv import load_dotenv

from job_platforms_APIs import HeadHunterApi, SuperJob


def run_head_hunter_analyzer(popular_programming_languages, hh_app_name, hh_app_email):
    headers = {'User-Agent': f'{hh_app_name}-{hh_app_email}'}
    base_url = 'https://api.hh.ru/'
    area_id = 2  # saint petersburg
    period = 30

    analyzed_language_vacancies = {}

    hh_api = HeadHunterApi(base_url=base_url, headers=headers)
    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )

    for language in popular_programming_languages:
        search_text = f'Программист {language}'
        per_page = 100
        params = {
            'text': search_text,
            'professional_role': developer_role_id,
            'area': area_id,
            'period': period,
            'per_page': per_page,
        }
        all_vacancies = hh_api.get_all_vacancies(params=params)

        vacancies_found = len(all_vacancies)
        expected_salaries = hh_api.predict_rub_salary(all_vacancies)
        vacancies_processed = len(expected_salaries)
        average_salary = sum(expected_salaries) / vacancies_processed

        analyzed_vacancies = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary),
        }

        analyzed_language_vacancies[f'{language}'] = analyzed_vacancies
    print(analyzed_language_vacancies)


def run_super_job_analyzer(popular_programming_languages, client_id, secret_key, code):
    headers = {'X-Api-App-Id': secret_key}
    base_url = 'https://api.superjob.ru/2.0/'
    town = 'Санкт-Петербург'
    catalogues = 33

    api_instance = SuperJob(base_url=base_url, headers=headers)
    api_instance.get_authorize(client_id=client_id)
    api_instance.get_access_token(client_id=client_id, secret_key=secret_key, code=code)

    for language in popular_programming_languages:
        search_text = f'Программист {language}'
        all_vacancies = api_instance.get_vacancies(
            client_id=client_id, secret_key=secret_key, catalogues=catalogues,
            keyword=search_text, town=town
        )
        expected_salaries = api_instance.predict_rub_salary(all_vacancies)
        vacancies_found = len(all_vacancies)
        vacancies_processed = len(expected_salaries)
        average_salary = sum(expected_salaries) / vacancies_processed
        analyzed_vacancies = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary),
        }


def main():
    """The main logic for running the whole program."""
    load_dotenv()
    hh_app_name = os.environ.get("HH_APP_NAME")
    hh_app_email = os.environ.get("HH_APP_EMAIL")
    sj_client_id = int(os.environ.get("SUPER_JOB_CLIENT_ID"))
    sj_secret_key = os.environ.get("SUPER_JOB_SECRET_KEY")
    sj_code = os.environ.get("CODE")
    popular_programming_languages = ['JavaScript', 'C#', 'Java',
                                     'Python', 'PHP', 'TypeScript',
                                     'Kotlin', 'Swift', 'C++', 'Go']

    run_head_hunter_analyzer(
        popular_programming_languages=popular_programming_languages, hh_app_name=hh_app_name,
        hh_app_email=hh_app_email
    )
    run_super_job_analyzer(
        popular_programming_languages=popular_programming_languages, client_id=sj_client_id,
        secret_key=sj_secret_key, code=sj_code
    )


if __name__ == '__main__':
    main()
