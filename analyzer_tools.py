"""Module with functions, that helps analyze vacancies"""
from typing import Union

from terminaltables import AsciiTable


def get_statistics(api, programming_languages: list, search_key: str, vacancies_params: dict):
    """Get vacancies with certain page.
    :param api: - The instance of an API.
    :param programming_languages: - The most popular programming languages that we analyze.
    :param search_key: - The searching key for found vacancies.
    :param vacancies_params: - Necessary information for getting vacancies.
    :returns: statistics - Analyzed vacancies with info about of found, processed vacancies and average salary.
    """
    statistics = {}
    class_name = api.__class__.__name__

    for language in programming_languages:
        search_text = f'Программист {language}'
        vacancies_params.update({search_key: search_text})

        if class_name == 'SuperJob':
            all_vacancies = api.get_vacancies(params=vacancies_params)
            is_super_job = True
        else:
            all_vacancies = api.get_all_vacancies(params=vacancies_params)
            is_super_job = False

        expected_salaries = predict_rub_salary(vacancies=all_vacancies, super_job_indicator=is_super_job)
        vacancies_found = len(all_vacancies)
        vacancies_processed = len(expected_salaries)

        if vacancies_found and vacancies_processed:
            average_salary = sum(expected_salaries) / vacancies_processed
            analyzed_vacancies = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': int(average_salary),
            }
            statistics[f'{language}'] = analyzed_vacancies

    return statistics


def predict_rub_salary(vacancies, super_job_indicator):
    """Predict salary based on start or end salary range.
    :param vacancies: - All vacancies that we need to analyze.
    :param super_job_indicator: - The indicator, that show us what is API service we work with.
    :returns: expected_salaries - salary that we expected from start or end salary range.
    """
    expected_salaries = []

    for vacancy in vacancies:
        if not super_job_indicator:
            salary = vacancy['salary']

            if not salary:
                continue

            currency = salary['currency']
            start_salary = salary['from']
            end_salary = salary['to']
        else:
            currency = vacancy['currency']
            start_salary = vacancy['payment_from']
            end_salary = vacancy['payment_to']

        expected_salary = predict_salary(
            currency=currency, start_salary=start_salary, end_salary=end_salary
        )
        if expected_salary:
            expected_salaries.append(expected_salary)

    return expected_salaries


def predict_salary(currency: str, start_salary: int, end_salary: int) -> Union[float, None]:
    """Predict salary based on start or end salary range.
    :param currency: - Statistics of analyzed vacancies.
    :param start_salary: - The title of the table.
    :param end_salary: - The title of the table.
    :returns: expected_salary - salary that we expected from start or end salary range.
    """
    expected_salary = None
    currency_names = ('RUR', 'rub')

    if currency not in currency_names:
        return
    if start_salary and end_salary:
        expected_salary = (start_salary + end_salary) / 2
    elif start_salary:
        expected_salary = start_salary * 1.2
    elif not start_salary and end_salary:
        expected_salary = end_salary * 0.8

    return expected_salary


def show_statistics(statistics, title):
    """Show statistics of analyzed vacancies from HeadHunter and Super Job platforms.
    :param statistics: - Statistics of analyzed vacancies.
    :param title: - The title of the table.
    """
    table_data = [
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')
    ]
    for language, vacancies_statistics in statistics.items():
        vacancies_found = vacancies_statistics['vacancies_found']
        vacancies_processed = vacancies_statistics['vacancies_processed']
        average_salary = vacancies_statistics['average_salary']
        table_data.append([language, vacancies_found, vacancies_processed, average_salary])

    hh_table = AsciiTable(table_data=table_data, title=title)
    print(hh_table.table)
