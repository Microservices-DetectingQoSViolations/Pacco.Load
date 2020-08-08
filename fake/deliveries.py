from faker import Faker
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def start_delivery(order_id, date):
    return {
        "orderId": order_id,
        "description": fake_description(),
        "dateTime": date
    }


def fail(delivery_id):
    return {
        "id": delivery_id,
        "reason": fake_description()
    }


def registrations(delivery_id, date):
    return {
        "id": delivery_id,
        "description": fake_description(),
        "dateTime": date
    }


def complete(delivery_id):
    return {
        "id": delivery_id
    }


def fake_description():
    return ' '.join(faker.words(faker.random.randint(0, 15)))
