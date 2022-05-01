from dotenv import load_dotenv

from apis_constants import HH_BASE_API_URL, HH_HEADERS
from job_platforms_APIs import HeadHunterApi


def run_vacancies_analyzer():
    hh_api = HeadHunterApi(base_url=HH_BASE_API_URL, headers=HH_HEADERS)
    saint_petersburg = 2

    professional_roles = hh_api.get_professional_roles()
    developer_role_id = hh_api.get_role_id(
        query_industry='Информационные технологии',
        query_job='Программист',
        roles=professional_roles,
    )
    developer_vacancies = hh_api.get_vacancies(role_id=developer_role_id, area_id=saint_petersburg)
    return developer_vacancies


def main():
    """The main logic for running the whole program."""
    load_dotenv()


    run_vacancies_analyzer()


if __name__ == '__main__':
    main()
