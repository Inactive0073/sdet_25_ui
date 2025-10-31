# BankingProject UI autotests

Проект: UI автотесты для https://www.globalsqa.com/angularJs-protractor/BankingProject

## Требования
- Python 3.10
- хром (как под CI — используется webdriver-manager)

## Запуск локально
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. pytest (конфиг описан в pytest.ini)


## Allure
После запуска:
- `allure serve allure-results`  — локально запустить отчет
