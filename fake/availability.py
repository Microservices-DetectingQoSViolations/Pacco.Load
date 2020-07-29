from faker import Faker
from fake.predefined_fake_data import tags
from fake.settings import fake_settings
from fake.fake_collection import fake_collection

faker = Faker()
Faker.seed(fake_settings['seed'])


def resources(resource_id):
    return {
        "resourceId": resource_id,
        "tags": fake_collection(tags)
    }


def browse_tags_data(matchAll):
    match = 'false'
    if matchAll:
        if bool(faker.random.getrandbits(1)):
            match = 'true'

    return match, fake_collection(tags)[:2]


def reservations(resource_id, customer_id, date_time):
    return {
        "resourceId": resource_id,
        "customer_id": customer_id,
        "dateTime": date_time,
        "priority": faker.random.randint(0, 3)
    }


def get_priority():
    return {
        "priority": faker.random.randint(0, 3)
    }
