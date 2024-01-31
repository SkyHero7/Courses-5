import requests

def get_vacancies_from_hh(company_name):
    url = "https://api.hh.ru/vacancies"
    params = {
        'text': f'компания:{company_name}',
        'per_page': 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies_data = response.json()
        return vacancies_data['items']
    else:
        print(f"Failed to retrieve vacancies for {company_name}. Status code: {response.status_code}")
        return []

def get_vacancies_with_keyword_from_hh(keyword):
    url = "https://api.hh.ru/vacancies"
    params = {
        'text': keyword,
        'per_page': 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        vacancies_data = response.json()
        return vacancies_data['items']
    else:
        print(f"Failed to retrieve vacancies with keyword {keyword}. Status code: {response.status_code}")
        return []