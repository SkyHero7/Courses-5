import psycopg2
from psycopg2 import sql

class DBManager:
    """
      Класс для управления операциями с базой данных.
      """
    def __init__(self, dbname='north', user='postgres', password='1234', host='localhost', port=5432):
        """
                Инициализирует объект DBManager с параметрами соединения.

                :param dbname: str, название базы данных.
                :param user: str, имя пользователя для доступа к базе данных.
                :param password: str, пароль для доступа к базе данных.
                :param host: str, имя хоста сервера базы данных.
                :param port: int, номер порта сервера базы данных.
                """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Создает таблицы базы данных, если они не существуют."""

        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            description TEXT
        )
        """
        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            company_id INT NOT NULL,
            title VARCHAR NOT NULL,
            salary NUMERIC,
            link VARCHAR,
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
        """
        self.cursor.execute(create_companies_table)
        self.cursor.execute(create_vacancies_table)
        self.conn.commit()

    def insert_company(self, name, description=None):
        """
        Вставляет новую компанию в таблицу companies.

        :param name: str, название компании.
        :param description: str, необязательное описание компании.
        """
        insert_query = sql.SQL("INSERT INTO companies (name, description) VALUES (%s, %s)")
        self.cursor.execute(insert_query, (name, description))
        self.conn.commit()

    def insert_vacancy(self, company_id, title, salary=None, link=None):
        """
        Вставляет новую вакансию в таблицу vacancies.

        :param company_id: int, ID компании, связанной с вакансией.
        :param title: str, заголовок вакансии.
        :param salary: float, необязательная зарплата для вакансии.
        :param link: str, необязательная ссылка на вакансию.
        """
        query = "SELECT * FROM vacancies WHERE title = %s AND company_id = %s"
        self.cursor.execute(query, (title, company_id))
        existing_vacancy = self.cursor.fetchone()

        if not existing_vacancy:
            insert_query = sql.SQL("INSERT INTO vacancies (company_id, title, salary, link) VALUES (%s, %s, %s, %s)")
            self.cursor.execute(insert_query, (company_id, title, salary, link))
            self.conn.commit()

    def get_company_id_by_name(self, company_name):
        query = "SELECT company_id FROM companies WHERE name = %s"
        self.cursor.execute(query, (company_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_avg_salary(self):
        query = "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        query = "SELECT company_id, title, salary, link FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL);"
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        vacancies = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return vacancies

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
