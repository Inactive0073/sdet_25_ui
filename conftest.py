import os
import shutil
import tempfile
import uuid
from typing import Any, Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.config import get_test_config


def _build_chrome_options(headless: bool) -> ChromeOptions:
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")

    chrome_binary = os.getenv("CHROME_BIN")
    if chrome_binary:
        chrome_options.binary_location = chrome_binary

    return chrome_options


def _build_local_driver(chrome_options: ChromeOptions) -> WebDriver:
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
    chrome_service = (
        ChromeService(executable_path=chromedriver_path)
        if chromedriver_path
        else ChromeService(ChromeDriverManager().install())
    )
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def _build_remote_driver(
    chrome_options: ChromeOptions, remote_url: str
) -> webdriver.Remote:
    chrome_options.set_capability("enableVNC", True)
    chrome_options.set_capability("screenResolution", "1920x1080x24")
    return webdriver.Remote(command_executor=remote_url, options=chrome_options)


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
    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    test_config = get_test_config()
    if "windows" not in test_config.os and not remote_url:
        headless = True
    if browser == "chrome":
        chrome_options = _build_chrome_options(headless=headless)
        if not remote_url:
            user_data_dir = tempfile.mkdtemp(prefix=f"chrome-profile-{uuid.uuid4()}-")
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        driver = (
            _build_remote_driver(chrome_options, remote_url)
            if remote_url
            else _build_local_driver(chrome_options)
        )
        driver.set_window_size(1920, 1080)
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
