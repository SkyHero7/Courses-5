from db_manager import DBManager
from hh_api import get_vacancies_from_hh, get_vacancies_with_keyword_from_hh


def main():
    """
    Основная функция программы для управления операциями с базой данных и вакансиями.
    """
    db_manager = DBManager()

    search_option = input(
        "Введите 'company' для поиска по названию компании, или 'keyword' для поиска по ключевому слову: ")

    if search_option == 'keyword':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies = get_vacancies_with_keyword_from_hh(keyword)

        if vacancies:
            print("Найденные вакансии на HeadHunter:")
            for vacancy in vacancies:
                print(f"Название: {vacancy['name']}, Ссылка: {vacancy['alternate_url']}")
        else:
            print("Нет результатов на HeadHunter.")

        print("Найденные вакансии в базе данных:")
        db_vacancies = db_manager.get_vacancies_with_keyword(keyword)
        for vacancy in db_vacancies:
            print(f"Название: {vacancy['title']}, Ссылка: {vacancy['link']}")



    elif search_option == 'company':
        company_name = input("Введите название компании: ")
        vacancies = get_vacancies_from_hh(company_name)

        if vacancies:
            print(f"Вакансии компании {company_name}:")
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
            print(f"Нет вакансий для компании {company_name}")

    else:
        print("Некорректный выбор.")

    print("Средняя зарплата по вакансиям:", db_manager.get_avg_salary())

    print("Список вакансий с зарплатой выше средней:")
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in higher_salary_vacancies:
        print(vacancy)

    print("Информация о компаниях и числе вакансий:")
    companies_info = db_manager.get_companies_and_vacancies_count()
    for company_info in companies_info:
        print(f"Компания: {company_info[0]}, Количество вакансий: {company_info[1]}")

    db_manager.close_connection()


if __name__ == "__main__":
    main()
