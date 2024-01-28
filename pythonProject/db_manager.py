import psycopg2
from psycopg2 import sql

class DBManager:
    def __init__(self, dbname='north', user='postgres', password='1234', host='localhost', port=5432):
        self.conn = psycopg2.connect(
            dbname='north',
            user='postgres',
            password='1234',
            host='localhost',
            port='5432'
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
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
        insert_query = sql.SQL("INSERT INTO companies (name, description) VALUES (%s, %s)")
        self.cursor.execute(insert_query, (name, description))
        self.conn.commit()

    def insert_vacancy(self, company_id, title, salary=None, link=None):
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
