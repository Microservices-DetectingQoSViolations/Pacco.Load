from faker import Faker
from fake.predefined_fake_data import tags
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def resources(resource_id):
    res_tags = []
    times = faker.random.randint(1, len(tags) - 1)


    return {
        "resourceId": resource_id,
        "tags": list(set(res_tags))
    }


def reservations(resource_id, customer_id, date_time):
    return {
        "resourceId": resource_id,
        "customer_id": customer_id,
        "dateTime": date_time,
        "priority": faker.random.randint(0, 4)
    }
