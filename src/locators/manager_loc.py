from selenium.webdriver.common.by import By


class ManagerLocators:
    BANK_MANAGER_LOGIN_BUTTON = (
        By.XPATH,
        "//button[@ng-click='manager()']",
    )  # Доступна при авторизации

    ADD_CUSTOMER_BUTTON = (By.XPATH, "//button[@ng-click='addCust()']")
    OPEN_ACCOUNT_BUTTON = (By.XPATH, "//button[@ng-click='openAccount()']")
    CUSTOMERS_LIST_BUTTON = (By.XPATH, "//button[@ng-click='showCust()']")


class AddCustomerLocators(ManagerLocators):
    FIRST_NAME_INPUT = (By.XPATH, "//input[@ng-model='fName']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@ng-model='lName']")
    POSTAL_CODE_INPUT = (By.XPATH, "//input[@ng-model='postCd']")
    SUBMIT_ADD_CUSTOMER_BUTTON = (By.XPATH, "//button[@type='submit']")


class CustomersListLocators(ManagerLocators):
    CUSTOMER_ROWS = (By.XPATH, "//table//tbody//tr")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")
    FIRST_NAME_HEADER = (By.XPATH, "//thead/tr[1]/td[1]/a")

    FIRST_NAME_CELL = (By.XPATH, "./td[1]")
    DELETE_BUTTON = (By.XPATH, ".//button[@ng-click='deleteCust(cust)']")
