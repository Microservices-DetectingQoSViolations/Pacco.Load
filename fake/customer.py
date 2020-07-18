from faker import Faker
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def create_customer():
    return {
        "fullName": faker.name(),
        "address": faker.address()
    }
