from dataclasses import dataclass


@dataclass
class TestConfig:
    page_load_timeout: int
    implicit_wait: int


def get_test_config(page_load_timeout: int = 10, implicit_wait: int = 5) -> TestConfig:
    return TestConfig(page_load_timeout=page_load_timeout, implicit_wait=implicit_wait)
