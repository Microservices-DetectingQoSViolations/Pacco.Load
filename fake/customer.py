from faker import Faker

faker = Faker()
Faker.seed(1)


def create_customer():
    return {
        "fullName": faker.name(),
        "address": faker.address()
    }
