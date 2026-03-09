import allure
from selenium.webdriver.remote.webdriver import WebDriver

from src.data import URLs
from src.pages.add_customer_page import AddCustomerPage
from src.pages.customers_list_page import CustomersListPage
from src.pages.manager_page import ManagerPage
from src.schema.customer import Customer


class CustomerActions:
    def __init__(self, driver: WebDriver):
        self.manager = ManagerPage(driver)
        self.add_customer = AddCustomerPage(driver)
        self.customers = CustomersListPage(driver)

    @allure.step("Перейти в менеджерский раздел")
    def open_manager(self) -> None:
        """Открыть страницу менеджера"""
        self.manager.open(URLs.MANAGER_URL)
        self.manager.click_bank_manager_login()

    @allure.step("Открыть форму добавления клиента")
    def open_add_customer_form(self) -> None:
        """Открыть форму добавления клиента"""
        self.add_customer.open(URLs.MANAGER_URL)
        self.manager.click_add_customer()

    @allure.step("Открыть список клиентов")
    def open_customers_list(self) -> None:
        """Открыть список клиентов"""
        self.customers.open(URLs.MANAGER_URL)
        self.manager.click_customers()

    @allure.step("Создать клиента: ")
    def create_customer(self, customer: Customer) -> str:
        """Создать клиента"""
        self.open_add_customer_form()
        self.add_customer.fill_first_name(customer.first_name)
        self.add_customer.fill_last_name(customer.last_name)
        self.add_customer.fill_postal_code(customer.post_code)
        self.add_customer.click_submit()
        text = self.add_customer.accept_alert_and_get_text()
        return text

    @allure.step("Получить все имена клиентов")
    def get_all_first_names(self) -> list[str]:
        """Получить все имена клиентов"""
        self.open_customers_list()
        return self.customers.get_all_first_names()

    @allure.step("Удалить клиента по имени: {name}")
    def delete_customer_by_name(self, name: str) -> None:
        """Удалить клиента по имени"""
        self.open_customers_list()
        self.customers.delete_customer_by_name(name)

    @allure.step("Убедиться, что есть минимум {count} клиентов")
    def ensure_customers_exist(self, count: int = 3):
        """Создать клиентов, если их меньше {count}"""
        self.open_customers_list()
        if len(set(map(str.lower, self.customers.get_all_first_names()))) < count:
            for _ in range(count):
                self.create_customer(Customer.random())

    @allure.step("Получить имена клиентов в порядке Z→A")
    def get_names_sorted_desc(self) -> list[str]:
        """Получить имена клиентов в порядке Z→A"""
        self.open_customers_list()
        self.customers.click_first_name_header()
        return self.customers.get_all_first_names()

    @allure.step("Получить имена клиентов в порядке A→Z")
    def get_names_sorted_asc(self) -> list[str]:
        """Получить имена клиентов в порядке A→Z"""
        self.open_customers_list()
        self.customers.click_first_name_header()
        self.customers.click_first_name_header()  # реверс
        return self.customers.get_all_first_names()

    @staticmethod
    @allure.step("Проверка сортировки по возрастанию")
    def is_sorted_asc(names: list[str]) -> bool:
        return names == sorted(names)

    @staticmethod
    @allure.step("Проверка сортировки по убыванию")
    def is_sorted_desc(names: list[str]) -> bool:
        return names == sorted(names, reverse=True)
