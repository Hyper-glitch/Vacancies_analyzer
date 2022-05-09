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


def get_analyzed_vacancies(api, programming_languages: list, search_key: str, vacancies_params: dict):
    analyzed_language_vacancies = {}
    super_job_indicator = 'keyword'

    for language in programming_languages:
        search_text = f'Программист {language}'
        vacancies_params.update({search_key: search_text})

        if search_key == super_job_indicator:
            all_vacancies = api.get_vacancies(params=vacancies_params)
        else:
            all_vacancies = api.get_all_vacancies(params=vacancies_params)

        expected_salaries = api.predict_rub_salary(all_vacancies)
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
