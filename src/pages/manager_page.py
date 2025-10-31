import allure

from src.locators.manager_loc import ManagerLocators as ML
from src.pages.base_page import BasePage


class ManagerPage(BasePage):
    BANK_MANAGER_LOGIN_BUTTON = ML.BANK_MANAGER_LOGIN_BUTTON
    ADD_CUSTOMER_BUTTON = ML.ADD_CUSTOMER_BUTTON
    CUSTOMERS_LIST_BUTTON = ML.CUSTOMERS_LIST_BUTTON

    @allure.step("Клик: Bank Manager Login")
    def click_bank_manager_login(self) -> None:
        self.click(self.BANK_MANAGER_LOGIN_BUTTON)

    @allure.step("Клик: Add Customer")
    def click_add_customer(self) -> None:
        self.click(self.ADD_CUSTOMER_BUTTON)

    @allure.step("Клик: Customers")
    def click_customers(self) -> None:
        self.click(self.CUSTOMERS_LIST_BUTTON)
