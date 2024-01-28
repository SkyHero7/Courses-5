from src.api import HeadHunterAPI, SuperJobAPI
from src.json_saver import JSONSaver

def interact_with_user(json_saver):
    platform, keyword = json_saver.get_user_input()

    if platform == "superjob":
        vacancies = json_saver.superjob_api.get_vacancies(keyword)
    elif platform == "hh":
        vacancies = json_saver.hh_api.get_vacancies(keyword)
    else:
        print("Неверная платформа. Выберите superjob или hh.")
        return

    print('DEBUG_1', vacancies)  # добавил_1
    for item in vacancies:
        if isinstance(item, dict):
            print('DEBUG_2')  # добавил_2
            print(item.get('name'), item.get('salary'), item.get('description'))

def main():
    hh_api_key = "api_key_для_HeadHunter"
    superjob_api_key = SuperJobAPI(api_key='3276', secret_key="v3.r.138050817.4c3855a0639d54c0922748478bd393d6c3e2764e.4e47dd609f838b394fcde97a447ddaf974b7eb92")

    hh_api = HeadHunterAPI(hh_api_key)
    superjob_api = SuperJobAPI(superjob_api_key)

    hh_vacancies = hh_api.get_vacancies("Python")
    superjob_vacancies = superjob_api.get_vacancies("Python")

    print(hh_vacancies)
    print(superjob_vacancies)


if __name__ == "__main__":
    superjob_api = SuperJobAPI(api_key="3276", secret_key="v3.r.138050817.4c3855a0639d54c0922748478bd393d6c3e2764e.4e47dd609f838b394fcde97a447ddaf974b7eb92")
    hh_api = HeadHunterAPI(api_key="P2V4KSUBEL7SVA1A4B1FQDBD80KQI3I1J0ICHSJB4232UGAV7JS0JJO9POORBVA6")
    json_saver = JSONSaver(superjob_api, hh_api, "vacancies.json")

    interact_with_user(json_saver)