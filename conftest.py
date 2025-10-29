import tempfile
import uuid
import pytest
import allure
from typing import Any, Generator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver


from webdriver_manager.chrome import ChromeDriverManager

from src.utils.config import get_test_config


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser: chrome"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run headless"
    )


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, Any, Any]:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    test_config = get_test_config()
    if browser == "chrome":
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        user_data_dir = tempfile.mkdtemp(prefix=f"chrome-profile-{uuid.uuid4()}-")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.set_page_load_timeout(test_config.page_load_timeout)
        driver.implicitly_wait(test_config.implicit_wait)

    else:
        raise ValueError("Only chrome is supported in this case")

    yield driver
    with allure.step("Закрываем браузер"):
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, None, None]:
    outcome = yield
    rep: pytest.TestReport = outcome.get_result()  # type: ignore

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")  # type: ignore
        if driver:
            try:
                png = driver.get_screenshot_as_png()
                allure.attach(
                    png,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
