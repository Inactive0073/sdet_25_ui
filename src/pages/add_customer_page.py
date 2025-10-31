import allure

from src.locators.manager_loc import AddCustomerLocators as ACL

from .base_page import BasePage


class AddCustomerPage(BasePage):
    FIRST_NAME_INPUT = ACL.FIRST_NAME_INPUT
    LAST_NAME_INPUT = ACL.LAST_NAME_INPUT
    POSTAL_CODE_INPUT = ACL.POSTAL_CODE_INPUT
    SUBMIT_ADD_CUSTOMER_BUTTON = ACL.SUBMIT_ADD_CUSTOMER_BUTTON

    @allure.step("Кликнуть Add Customer")
    def click_add_customer(self, locator: tuple[str, str]) -> None:
        self.click(locator)

    @allure.step("Заполнить First Name")
    def fill_first_name(self, text: str) -> None:
        "Заполнение имени"
        self.enter_text(self.FIRST_NAME_INPUT, text)

    @allure.step("Заполнить Last Name")
    def fill_last_name(self, text: str) -> None:
        "Заполнение фамилии"
        self.enter_text(self.LAST_NAME_INPUT, text)

    @allure.step("Заполнить Postal Code")
    def fill_postal_code(self, text: str) -> None:
        "Заполнение почтового индекса"
        self.enter_text(self.POSTAL_CODE_INPUT, text)

    @allure.step("Кликнуть на кнопку Submit")
    def click_submit(self) -> None:
        "Клик по кнопке Submit"
        self.click(self.SUBMIT_ADD_CUSTOMER_BUTTON)

    @allure.step("Принять alert и вернуть его текст")
    def accept_alert_and_get_text(self) -> str:
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text
