from db_manager import DBManager
from hh_api import get_vacancies_from_hh, get_vacancies_with_keyword_from_hh

if __name__ == "__main__":
    dbname = input("Введите имя базы данных: ")
    user = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    db_manager = DBManager(dbname=dbname, user=user, password=password)

    search_option = input(
        "Введите 'company' для поиска по названию компании, или 'keyword' для поиска по ключевому слову: ")

    if search_option == 'keyword':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies = get_vacancies_with_keyword_from_hh(keyword)

        if vacancies:
            print("Найденные вакансии:")
            for vacancy in vacancies:
                company_name = vacancy.get('employer', {}).get('name', 'Unknown')
                title = vacancy.get('name', 'Unknown')
                if vacancy and vacancy.get('salary'):
                    salary = vacancy['salary'].get('from')
                else:
                    salary = None
                link = vacancy.get('alternate_url', 'Нет ссылки')

                print(
                    f"Компания: {company_name}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

                company_id = db_manager.get_company_id_by_name(company_name)
                if not company_id:
                    db_manager.insert_company(company_name)
                    company_id = db_manager.get_company_id_by_name(company_name)

                db_manager.insert_vacancy(company_id, title, salary, link)
        else:
            print("Нет результатов.")

    elif search_option == 'company':
        company_name = input("Введите название компании: ")
        vacancies = get_vacancies_from_hh(company_name)

        if vacancies:
            print(f"Вакансии компании {company_name}:")
            for vacancy in vacancies:
                company_name = vacancy.get('employer', {}).get('name', 'Unknown')
                title = vacancy.get('name', 'Unknown')
                salary = vacancy.get('salary', {}).get('from', 'Не указана')
                link = vacancy.get('alternate_url', 'Нет ссылки')

                print(
                    f"Компания: {company_name}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

                company_id = db_manager.get_company_id_by_name(company_name)
                if not company_id:
                    db_manager.insert_company(company_name)
                    company_id = db_manager.get_company_id_by_name(company_name)

                db_manager.insert_vacancy(company_id, title, salary, link)
        else:
            print(f"Нет вакансий для компании {company_name}")

    else:
        print("Некорректный выбор.")

    print("Средняя зарплата по вакансиям:", db_manager.get_avg_salary())

    print("Список вакансий с зарплатой выше средней:")
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in higher_salary_vacancies:
        print(vacancy)

    db_manager.close_connection()