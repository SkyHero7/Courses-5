import psycopg2
from psycopg2 import sql

# Параметры подключения к БД
connection_params = {
    'dbname': 'north',
    'user': 'ваше_имя_пользователя',
    'password': 'ваш_пароль',
    'host': 'ваш_хост',
    'port': 'ваш_порт'
}

# Подключение к БД
connection = psycopg2.connect(**connection_params)
cursor = connection.cursor()

# Вставка данных в таблицу employees
cursor.execute("INSERT INTO employees (first_name, last_name, hire_date) VALUES (%s, %s, %s)",
               ('John', 'Doe', '2022-01-01'))

# Вставка данных в таблицу customers
cursor.execute("INSERT INTO customers (company_name, contact_name, country) VALUES (%s, %s, %s)",
               ('ABC Inc.', 'Alice', 'USA'))

# Вставка данных в таблицу orders
cursor.execute("INSERT INTO orders (order_date, employee_id, customer_id) VALUES (%s, %s, %s)",
               ('2022-01-15', 1, 1))

# Сохранение изменений и закрытие соединения
connection.commit()
cursor.close()
connection.close()