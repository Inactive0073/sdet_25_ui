# actions/customer_actions.py
import allure
from src.pages.manager_page import ManagerPage
from pages.add_customer_page import AddCustomerPage
from pages.customers_list_page import CustomersListPage
from selenium.webdriver.remote.webdriver import WebDriver

from src.schema.customer import Customer


class CustomerActions:

    def __init__(self, driver: WebDriver):
        self.manager = ManagerPage(driver)
        self.add_customer = AddCustomerPage(driver)
        self.customers = CustomersListPage(driver)

    @allure.step("Перейти в менеджерский раздел")
    def open_manager(self) -> None:
        self.manager.click_bank_manager_login()

    @allure.step("Открыть форму добавления клиента")
    def open_add_customer_form(self) -> None:
        self.manager.click_add_customer()

    @allure.step("Создать клиента: {customer.first_name} {customer.last_name}")
    def create_customer(self, customer: Customer) -> str:
        self.open_add_customer_form()
        self.add_customer.fill_first_name(customer.first_name)
        self.add_customer.fill_last_name(customer.last_name)
        self.add_customer.fill_postal_code(customer.post_code)
        self.add_customer.click_submit()
        # вернуть текст alert для проверки
        text = self.add_customer.accept_alert_and_get_text()
        return text

    @allure.step("Открыть список клиентов")
    def open_customers_list(self) -> None:
        self.manager.click_customers()

    @allure.step("Получить все имена клиентов")
    def get_all_first_names(self) -> list[str]:
        self.open_customers_list()
        return self.customers.get_all_first_names()

    @allure.step("Удалить клиента по имени: {name}")
    def delete_customer_by_name(self, name: str) -> None:
        self.open_customers_list()
        self.customers.delete_customer_by_name(name)
