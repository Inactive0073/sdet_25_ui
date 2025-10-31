import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.actions.manager_actions import CustomerActions as CA
from src.services.customer_service import find_name_closest_to_average_length

from .assert_helper import assert_not_in


@allure.epic("BankingProject")
@allure.feature("Удаление клиента")
@allure.story("Удаление клиента")
@allure.title("TC-003 Удаление клиента, длина имени ближе всего к среднему")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Страница удаления клиента")
@allure.tag("customer_sorting")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.ui
class TestDeleteCustomer:
    """Тесты удаления клиентов с тем именем, у которого длина будет ближе
    к среднему арифметическому  в приложении XYZ Bank."""

    @allure.title("TC-003: Удаление клиента, длина имени ближе к среднему")
    def test_delete_customer_closest_to_avg(self, driver: WebDriver):
        customer_actions = CA(driver)

        customer_actions.ensure_customers_exist(3)

        names = customer_actions.get_all_first_names()
        name_to_delete = find_name_closest_to_average_length(names)
        customer_actions.delete_customer_by_name(name_to_delete)

        names_after = customer_actions.get_all_first_names()
        assert_not_in(
            name_to_delete,
            names_after,
            f"Ожидалось, что имя '{name_to_delete}' удалено",
        )
