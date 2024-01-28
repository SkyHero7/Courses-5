from abc import ABC, abstractmethod
from typing import List, Dict
from urllib.parse import urlencode
import requests
from .models import Vacancy

class AbstractVacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query: str) -> List[Dict]:
        raise NotImplementedError("Subclasses must implement this method.")

class HeadHunterAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword):
        params = {
            "text": keyword,
            "api_key": self.api_key,
        }
        response = requests.get(self.base_url, params=params)

        return response.json()



class SuperJobAPI:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            "X-Api-App-Id": self.api_key,
            "X-Api-Secret-Id": self.secret_key,
        }

    def _fetch_vacancies_data(self, keyword):
        params = {"keyword": keyword}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        return response.json()

    def get_vacancies(self, keyword):
        vacancies_data = self._fetch_vacancies_data(keyword)
        return vacancies_data.get("items", [])