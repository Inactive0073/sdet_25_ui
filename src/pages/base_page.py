from typing import Generic, Sequence, TypeVar

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PageT = TypeVar("PageT", bound="BasePage")


class BasePage(Generic[PageT]):
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find(self, locator: tuple[str, str]) -> WebElement:
        try:
            return self.wait.until(
                EC.presence_of_element_located(locator),
                message=f"Не удалось найти элемент: {locator}",
            )
        except TimeoutException as e:
            allure.attach(
                str(e),
                name="TimeoutException",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise

    @allure.step("Найти элементы: {locator}")
    def find_all(self, locator: tuple[str, str]) -> Sequence[WebElement]:
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located(locator),
                message=f"Не удалось найти элементы: {locator}",
            )
        except TimeoutException as e:
            allure.attach(
                str(e),
                name="TimeoutException",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise

    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_element_visible(
        self, locator: tuple[str, str], timeout: int | None = None
    ):
        if timeout is not None:
            self.wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Не удалось дождаться видимости элемента: {locator}",
        )

    @allure.step("Ожидание кликабельности элемента: {locator}")
    def wait_for_element_clickable(
        self, locator: tuple[str, str], timeout: int | None = None
    ):
        if timeout is not None:
            self.wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Не удалось дождаться кликабельности элемента: {locator}",
        )

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator: tuple[str, str]):
        element = self.wait_for_element_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            # если элемент перекрыт или вне области видимости → скроллим и пробуем снова
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            try:
                element.click()
            except ElementClickInterceptedException:
                ActionChains(self.driver).move_to_element(element).click().perform()

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def enter_text(
        self, locator: tuple[str, str], text: str, timeout: int | None = None
    ):
        if self.is_element_present(locator, timeout):
            element = self.find(locator)
            element.clear()
            with allure.step(f"Заполняем {locator} текстом: {text}"):
                element.send_keys(text)
        else:
            allure.attach(
                self.get_page_screenshot(),
                name="element_not_found_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                f"Элемент не найден: {locator}\nТекст для ввода: {text}",
                name="error_details",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.step("Получить текст из элемента {locator}")
    def get_text(self: PageT, locator: tuple[str, str]) -> str:
        element = self.find(locator)
        return element.text

    @allure.step("Проверить наличие элемента: {locator}")
    def is_element_present(
        self, locator: tuple[str, str], timeout: int | None = None
    ) -> bool:
        """Если таймаут не указан, используется дефолтное значение из utils/config.py на уровне драйвера"""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except Exception:
            return False

    def get_page_screenshot(self):
        return self.driver.get_screenshot_as_png()
