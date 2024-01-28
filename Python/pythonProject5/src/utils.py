import json
from .models import Vacancy

class JSONSaver:
    def __init__(self, filename='vacancies.json'):
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy.__dict__)

    def save_to_json(self, data, filename):
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def load_from_json(self, filename):
        with open(filename, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def get_vacancies_by_keyword(self, keyword):
        superjob_vacancies = self.superjob_api.get_vacancies(keyword)
        hh_vacancies = self.hh_api.get_vacancies(keyword)
        return self.merge_and_filter_vacancies(superjob_vacancies, hh_vacancies)

    def get_user_input(self):
        platform = input("Введите платформу (superjob/hh): ")
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        return platform.lower(), keyword

    def get_vacancies_by_salary(self, min_salary, max_salary):
        min_salary = int(min_salary)
        max_salary = int(max_salary)
        return [
            Vacancy(**vacancy) for vacancy in self.vacancies
            if vacancy.get('salary') and self.is_valid_salary(vacancy['salary'])
               and min_salary <= self.extract_salary(vacancy['salary']) <= max_salary
        ]

    @staticmethod
    def is_valid_salary(salary):
        return '-' in salary and 'руб.' in salary

    @staticmethod
    def extract_salary(salary):
        return int(salary.split('-')[0].replace(' ', ''))

    def delete_vacancy(self, title):
        self.vacancies = [vacancy for vacancy in self.vacancies if vacancy['title'] != title]
        self.save_to_json()