import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.actions.manager_actions import CustomerActions as CA


@allure.epic("BankingProject")
@allure.feature("Сортировка клиентов")
@allure.story("Сортировка First Name")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Страница сортировки клиентов")
@allure.tag("customer_sorting")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.ui
class TestSorting:
    @allure.title("TC-002: Проверка сортировки First Name A→Z и Z→A")
    def test_sorting_by_first_name(self, driver: WebDriver):
        customer_actions = CA(driver)

        customer_actions.ensure_customers_exist(3)

        names_desc = customer_actions.get_names_sorted_desc()
        assert customer_actions.is_sorted_desc(names_desc), (
            f"Ожидали Z->A, получили: {names_desc}"
        )

        names_asc = customer_actions.get_names_sorted_asc()
        assert customer_actions.is_sorted_asc(names_asc), (
            f"Ожидали A->Z, получили: {names_asc}"
        )
