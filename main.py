import os

from dotenv import load_dotenv

from job_platforms_APIs import HeadHunterApi


def run_vacancies_analyzer(hh_app_name, hh_app_email):
    hh_headers = {'User-Agent': f'{hh_app_name}-{hh_app_email}'}
    hh_base_url = 'https://api.hh.ru/'
    area_id = 2  # saint petersburg
    period = 30
    popular_programming_languages = ['JavaScript', 'C#', 'Java',
                                     'Python', 'PHP', 'TypeScript',
                                     'Kotlin', 'Swift', 'C++', 'Go']
    analyzed_language_vacancies = {}

    hh_api = HeadHunterApi(base_url=hh_base_url, headers=hh_headers)
    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )

    for language in popular_programming_languages:
        search_text = f'Программист {language}'
        developer_vacancies = hh_api.get_vacancies(
            role_id=developer_role_id, area_id=area_id,
            period=period, text=search_text
        )

        all_vacancies = developer_vacancies['found']
        expected_salaries = hh_api.predict_rub_salary(developer_vacancies['items'])
        vacancies_processed = len(expected_salaries)
        average_salary = sum(expected_salaries) / vacancies_processed

        analyzed_vacancies = {
            'vacancies_found': all_vacancies,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary),
        }

        analyzed_language_vacancies[f'{language}'] = analyzed_vacancies


def main():
    """The main logic for running the whole program."""
    load_dotenv()
    hh_app_name = os.environ.get("HH_APP_NAME")
    hh_app_email = os.environ.get("HH_APP_EMAIL")

    run_vacancies_analyzer(hh_app_name=hh_app_name, hh_app_email=hh_app_email)


if __name__ == '__main__':
    main()
