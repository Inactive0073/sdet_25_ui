import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from tests.base_ui_test import BaseUITest

from src.actions.manager_actions import CustomerActions as CA
from src.schema.customer import Customer


@allure.epic("BankingProject")
@allure.feature("Добавление клиента")
@allure.story("Добавление нового клиента")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Страница добавления нового клиента")
@allure.tag("add_customer")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.ui
class TestAddCustomerPage(BaseUITest):
    """Тесты страницы 'Add Customer' в приложении XYZ Bank."""

    @allure.title(
        "TC-001 Создание клиента с Post Code 10 цифр и First Name из Post Code"
    )
    def test_add_customer(self, driver: WebDriver):
        customer = Customer.random()
        customer_actions = CA(driver)
        alert_text = customer_actions.create_customer(customer)
        assert "Customer added" in alert_text, (
            f"Ожидали 'Customer added' в alert, получили: '{alert_text}'"
        )

        names = customer_actions.get_all_first_names()
        self.assert_in(
            customer.first_name,
            names,
            f"Ожидалось, что имя {customer.first_name} появится в списке клиентов",
        )
