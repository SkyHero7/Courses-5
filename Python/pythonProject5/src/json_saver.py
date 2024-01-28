
import json
from typing import List, Dict

class JSONSaver:
    def __init__(self, superjob_api, hh_api, filename):
        self.superjob_api = superjob_api
        self.hh_api = hh_api
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, vacancy: 'Vacancy'):
        if vacancy.validate():
            self.vacancies.append({
                'title': vacancy.title,
                'link': vacancy.link,
                'salary': vacancy.salary,
                'description': vacancy.description
            })
            self._save_to_file()

    def save_vacancies_to_json(self, filename, vacancies):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(vacancies, json_file, ensure_ascii=False, indent=4)

    def get_vacancies_by_salary(self, min_salary, max_salary):
        superjob_vacancies = self.superjob_api.get_vacancies("Python")
        hh_vacancies = self.hh_api.get_vacancies("Python")

        filtered_vacancies = [
            vacancy for vacancy in superjob_vacancies + hh_vacancies
            if self.is_valid_salary(vacancy['salary']) and min_salary <= self.extract_salary(
                vacancy['salary']) <= max_salary
        ]

        return filtered_vacancies

    def is_valid_salary(self, salary):
        return '-' in salary and 'руб.' in salary
    def get_vacancies_by_criteria(self, criteria: str) -> List[Dict]:
        # Реализация получения вакансий из JSON-файла по критериям
        filtered_vacancies = [v for v in self.vacancies if criteria in v['description']]
        return filtered_vacancies

    def delete_vacancy(self, vacancy: 'Vacancy'):
        # Реализация удаления вакансии из JSON-файла
        self.vacancies = [v for v in self.vacancies if v != {
            'title': vacancy.title,
            'link': vacancy.link,
            'salary': vacancy.salary,
            'description': vacancy.description
        }]
        self._save_to_file()

    def _save_to_file(self):
        with open(self.filename, 'w') as file:
            json.dump(self.vacancies, file)

    def get_user_input(self):
        platform = input("Введите платформу (SuperJob или HeadHunter): ")
        keyword = input("Введите ключевое слово для поиска: ")
        return platform, keyword