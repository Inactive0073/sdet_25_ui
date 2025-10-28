# pages/customers_list_page.py
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
import allure
from typing import List

from src.locators.manager_loc import CustomersListLocators as CLL


class CustomersListPage(BasePage):
    CUSTOMER_ROWS = CLL.CUSTOMER_ROWS
    SEARCH_INPUT = CLL.SEARCH_INPUT
    FIRST_NAME_HEADER = CLL.FIRST_NAME_HEADER

    # selectors in table
    FIRST_ROW = CLL.FIRST_NAME_CELL
    DELETE_BUTTON = CLL.DELETE_BUTTON

    @allure.step("Получить First Name всех клиентов в таблице")
    def get_all_first_names(self) -> List[str]:
        rows = self.find_all(self.CUSTOMER_ROWS)
        names = []
        for r in rows:
            # FIRST_ROW is a locator tuple (By.XPATH, xpath); unpack when searching inside a row
            cell = r.find_element(*self.FIRST_ROW)
            text = cell.text.strip()
            # ignore empty cells (could be from non-data rows)
            if text:
                names.append(text)
        return names

    @allure.step("Найти строку клиента по имени: {name}")
    def find_row_by_first_name(self, name: str):
        rows = self.find_all(self.CUSTOMER_ROWS)
        for r in rows:
            cell = r.find_element(*self.FIRST_ROW)
            if cell.text.strip() == name:
                return r
        return None

    @allure.step("Удалить клиента по имени: {name}")
    def delete_customer_by_name(self, name: str) -> None:
        row = self.find_row_by_first_name(name)
        if not row:
            raise AssertionError(f"Клиент с именем '{name}' не найден для удаления")
        delete_btn = row.find_element(*self.DELETE_BUTTON)
        delete_btn.click()

    @allure.step("Клик по заголовку 'First Name' (сортировка)")
    def click_first_name_header(self) -> None:
        self.click(self.FIRST_NAME_HEADER)

    @allure.step("Поиск по клиентам: {text}")
    def search_customer(self, text: str) -> None:
        self.enter_text(self.SEARCH_INPUT, text)
