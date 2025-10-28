import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.actions.manager_actions import CustomerActions as CA
from src.schema.customer import Customer
from src.services.customer_service import find_name_closest_to_average_length
from .base_ui_test import BaseUITest


@allure.epic("BankingProject")
@allure.feature("Удаление клиента")
@allure.story("Удаление клиента")
@allure.title("TC-003 Удаление клиента, длина имени ближе всего к среднему")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Страница удаления клиента")
@allure.tag("customer_sorting")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.ui
class TestDeleteCustomer(BaseUITest):
    """Тесты удаления клиентов с тем именем, у которого длина будет ближе
    к среднему арифметическому  в приложении XYZ Bank."""

    @allure.title("TC-003: Удаление клиента, длина имени ближе к среднему")
    def test_delete_customer_closest_to_avg(self, driver: WebDriver):
        customer_actions = CA(driver)

        names = customer_actions.get_all_first_names()
        if len(names) < 3:
            for _ in range(3 - len(names)):
                customer = Customer.random()
                customer_actions.create_customer(customer)

        names = customer_actions.get_all_first_names()
        name_to_delete = find_name_closest_to_average_length(names)
        customer_actions.delete_customer_by_name(name_to_delete)

        names_after = customer_actions.get_all_first_names()
        self.assert_not_in(
            name_to_delete,
            names_after,
            f"Ожидалось, что имя '{name_to_delete}' удалено",
        )
