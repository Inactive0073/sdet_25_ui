import random

import allure


@allure.step("Генерация Post Code")
def generate_post_code() -> str:
    """Генерирует строку из 10 цифр."""
    return "".join(f"{random.randint(0, 9)}" for _ in range(10))


@allure.step("Генерация First Name из Post Code: {post_code}")
def generate_first_name(post_code: str) -> str:
    """
    Логика:
    - Разбиваем post_code на 5 двузначных сегментов (10 символов -> 5 сегментов)
    - Для каждого сегмента берем int(segment) % 26 и мапим 0->'a', 1->'b', ..., 25->'z'
    - Склеиваем буквы в имя (lowercase)
    """
    if len(post_code) != 10 or not post_code.isdigit():
        raise ValueError("post_code должен быть строкой из 10 цифр")
    letters = []
    for i in range(0, 10, 2):
        segment = post_code[i : i + 2]
        num = int(segment)
        idx = num % 26
        # буква по индексу (0 -> 'a')
        letter = chr(ord("a") + idx)
        letters.append(letter)
    return "".join(letters)
