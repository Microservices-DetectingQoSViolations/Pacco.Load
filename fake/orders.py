from faker import Faker
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def fake_order_date():
    return str(faker.date_this_year(before_today=False, after_today=True))


def assign_date(date):
    return {
        "deliveryDate": date
    }
