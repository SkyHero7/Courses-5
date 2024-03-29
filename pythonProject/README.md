# Описание проекта

Данный проект представляет собой программу для поиска вакансий с помощью API HeadHunter (HH) и сохранения информации о вакансиях в базу данных PostgreSQL.

## Файлы в проекте

- **main.py**: Основной файл программы, который выполняет поиск вакансий и сохраняет их в базу данных.
- **hh_api.py**: Модуль для взаимодействия с API HeadHunter.
- **db_manager.py**: Модуль для работы с базой данных PostgreSQL.
- **README.md**: Файл, который вы читаете сейчас. Содержит описание проекта.

## Работа программы

- Пользователь вводит параметры поиска (название компании или ключевое слово).
- Программа выполняет поиск вакансий с помощью API HeadHunter.
- Найденные вакансии сохраняются в базу данных PostgreSQL.
- Пользователю выводится список найденных вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию.

Установка
Создание виртуального окружения:

Для изоляции проекта и его зависимостей рекомендуется создать виртуальное окружение. Выполните следующую команду в корневой директории проекта:
python3 -m venv venv

Активация виртуального окружения:

В Windows:
venv\Scripts\activate

В macOS и Linux:
source venv/bin/activate

Установка зависимостей:

Установите необходимые зависимости из файла requirements.txt с помощью команды:
pip install -r requirements.txt
