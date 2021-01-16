from faker import Faker
from fake.settings import fake_settings
import random

mail_num = 0

def sign_up():
    faker = Faker()
    global mail_num
    mail_num = mail_num + 1
    return {
        "email": faker.ascii_safe_email() + str(mail_num),
        "password": faker.password(),
        "role": "user"
    }


def sign_in_invalid(password):
    seed = random.randint(0, 321312)
    Faker.seed(seed)
    faker = Faker()

    invalid = faker.password()
    while invalid == password:
        invalid = faker.password()
    return {
        "email": faker.ascii_safe_email(),
        "password": invalid
    }

