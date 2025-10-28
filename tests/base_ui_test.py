class BaseUITest:
    """
    Базовый класс для UI тестов.
    Содержит общие ассерт-хелперы и может содержать общий setup/teardown, если потребуется.
    """

    def assert_in(self, item, collection, message: str | None = None):
        if message is None:
            message = f"Ожидалось, что {item} присутствует в {collection}"
        assert item in collection, message

    def assert_not_in(self, item, collection, message: str | None = None):
        if message is None:
            message = f"Ожидалось, что {item} отсутствует в {collection}"
        assert item not in collection, message
