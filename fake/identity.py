from faker import Faker
from fake.settings import fake_settings

Faker.seed(fake_settings['seed'])
faker = Faker()


def sign_up():
    return {
        "email": faker.ascii_safe_email(),
        "password": faker.password(),
        "role": "user"
    }


def sign_in_invalid(password):
    invalid = faker.password()
    while invalid == password:
        invalid = faker.password()
    return {
        "email": faker.ascii_safe_email(),
        "password": invalid
    }

