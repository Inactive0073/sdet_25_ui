from dataclasses import dataclass


@dataclass
class URLs:
    LOGIN_URL: str = (
        "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
    )
    MANAGER_URL: str = (
        "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"
    )
    CUSTOMER_URL: str = (
        "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/customer"
    )
