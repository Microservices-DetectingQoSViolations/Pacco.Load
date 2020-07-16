from faker import Faker

faker = Faker()
faker.seed(4231)


def parcels(customer_id):
    return {
        "customer_id": customer_id,
        "variant": faker.name(),
        "size": faker.address(),
        "name": faker.name(),
        "description": faker.address()
    }
