from dataclasses import dataclass

from faker import Faker

from src.utils.data_generator import generate_first_name, generate_post_code

fake = Faker("en_US")


@dataclass
class Customer:
    first_name: str
    last_name: str
    post_code: str

    @classmethod
    def random(cls) -> "Customer":
        post_code = generate_post_code()
        first_name = generate_first_name(post_code)
        last_name = fake.last_name()
        return cls(first_name=first_name, last_name=last_name, post_code=post_code)
