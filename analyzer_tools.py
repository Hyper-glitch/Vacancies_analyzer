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

    return int(expected_salary) if expected_salary else None