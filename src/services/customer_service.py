import statistics
from typing import List

import allure


@allure.step("Поиск имени для удаления из списка {names}")
def find_name_closest_to_average_length(names: List[str]) -> str:
    """
    Возвращает имя, длина которого ближе всего к среднему арифметическому длин.
    При равном расстоянии возвращает первое по порядку.
    """
    if not names:
        raise ValueError("Список имен пуст")
    lengths = [len(n) for n in names]
    avg = statistics.mean(lengths)
    # минимизируем абсолютную разницу
    closest = min(names, key=lambda n: (abs(len(n) - avg), names.index(n)))
    return closest
