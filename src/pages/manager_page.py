from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

from src.locators.manager_loc import ManagerLocators as ML

class ManagerPage(BasePage):
    BANK_MANAGER_LOGIN_BUTTON = ML.BANK_MANAGER_LOGIN_BUTTON

    BANK_MANAGER_LOGIN_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Bank Manager Login')]",
    )
    ADD_CUSTOMER_BUTTON = (By.XPATH, "//button[contains(., 'Add Customer')]")
    OPEN_CUSTOMERS_BUTTON = (By.XPATH, "//button[contains(., 'Customers')]")

    @allure.step("Клик: Bank Manager Login")
    def click_bank_manager_login(self) -> None:
        self.click(self.BANK_MANAGER_LOGIN_BUTTON)

    @allure.step("Клик: Add Customer")
    def click_add_customer(self) -> None:
        self.click(self.ADD_CUSTOMER_BUTTON)

    @allure.step("Клик: Customers")
    def click_customers(self) -> None:
        self.click(self.OPEN_CUSTOMERS_BUTTON)
