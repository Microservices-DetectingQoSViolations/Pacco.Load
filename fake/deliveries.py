from faker import Faker
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def start_delivery(order_id, date):
    return {
        "orderId": order_id,
        "description": faker.words(faker.random.randint(0, 15)),
        "dateTime": date
    }


def fail(delivery_id):
    return {
        "id": delivery_id,
        "reason": faker.words(faker.random.randint(0, 15))
    }


def registrations(delivery_id, date):
    return {
        "id": delivery_id,
        "description": faker.words(faker.random.randint(0, 15)),
        "dateTime": date
    }


def complete(date):
    return {
        "id": date
    }
