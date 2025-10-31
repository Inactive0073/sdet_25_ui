"""
Базовый модуль для UI тестов.
Содержит общие ассерт-хелперы.
"""

def assert_in(item, collection, message: str | None = None):
    if message is None:
        message = f"Ожидалось, что {item} присутствует в {collection}"
    assert item in collection, message

def assert_not_in(item, collection, message: str | None = None):
    if message is None:
        message = f"Ожидалось, что {item} отсутствует в {collection}"
    assert item not in collection, message
