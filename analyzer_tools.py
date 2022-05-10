"""Module for functions, that helps analyze vacancies"""
from terminaltables import AsciiTable


def get_analyzed_vacancies(api, programming_languages: list, search_key: str, vacancies_params: dict):
    analyzed_language_vacancies = {}
    super_job_search_key = 'keyword'
    super_job_indicator = False

    for language in programming_languages:
        search_text = f'Программист {language}'
        vacancies_params.update({search_key: search_text})

        if search_key == super_job_search_key:
            all_vacancies = api.get_vacancies(params=vacancies_params)
            super_job_indicator = True
        else:
            all_vacancies = api.get_all_vacancies(params=vacancies_params)

        expected_salaries = predict_rub_salary(all_vacancies, super_job_indicator)
        vacancies_found = len(all_vacancies)
        vacancies_processed = len(expected_salaries)

        if vacancies_found and vacancies_processed:
            average_salary = sum(expected_salaries) / vacancies_processed
            analyzed_vacancies = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': int(average_salary),
            }
            analyzed_language_vacancies[f'{language}'] = analyzed_vacancies

    return analyzed_language_vacancies


def show_vacancies_statistics(analyzed_vacancies, title):
    table_data = [
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')
    ]
    for language, vacancies_statistics in analyzed_vacancies.items():
        vacancies_found = vacancies_statistics['vacancies_found']
        vacancies_processed = vacancies_statistics['vacancies_processed']
        average_salary = vacancies_statistics['average_salary']
        table_data.append([language, vacancies_found, vacancies_processed, average_salary])

    hh_table = AsciiTable(table_data=table_data, title=title)
    print(hh_table.table)


def predict_salary(currency, start_salary, end_salary, currency_name):
    expected_salary = None

    if currency != currency_name:
        return
    if start_salary and end_salary:
        expected_salary = (start_salary + end_salary) / 2
    elif start_salary:
        expected_salary = start_salary * 1.2
    elif not start_salary and end_salary:
        expected_salary = end_salary * 0.8

    return expected_salary


def predict_rub_salary(vacancies, super_job_indicator):
    expected_salaries = []

    for vacancy in vacancies:
        if not super_job_indicator:
            salary = vacancy['salary']

            if not salary:
                continue

            currency = salary['currency']
            start_salary = salary['from']
            end_salary = salary['to']
            currency_name = 'RUR'
        else:
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
