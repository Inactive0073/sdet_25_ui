import allure
import pytest

from .base_ui_test import BaseUITest


@allure.epic("BankingProject")
@allure.feature("Сортировка клиентов")
@allure.story("Сортировка First Name")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Страница сортировки клиентов")
@allure.tag("customer_sorting")
@allure.label("owner", "Alexey Yumanov")
@pytest.mark.ui
class TestSorting(BaseUITest):
    @allure.title("TC-002: Проверка сортировки First Name A→Z и Z→A")
    def test_sorting_by_first_name(self, customer_actions, data_generator):
        # Добавим несколько клиентов, чтобы гарантировать данные
        for _ in range(3):
            pc = data_generator.generate_post_code()
            fn = data_generator.generate_first_name(pc)
            customer_actions.create_customer(fn, "L", pc)

        # Проверка сортировки
        customer_actions.open_customers_list()
        # клик для сортировки A->Z
        customer_actions.customers.click_first_name_header()
        names_asc = customer_actions.customers.get_all_first_names()
        assert names_asc == sorted(names_asc), f"Ожидали A->Z, получили: {names_asc}"

        # клик для сортировки Z->A
        customer_actions.customers.click_first_name_header()
        names_desc = customer_actions.customers.get_all_first_names()
        assert names_desc == sorted(names_desc, reverse=True), (
            f"Ожидали Z->A, получили: {names_desc}"
        )
