from faker import Faker

faker = Faker()
faker.seed(4231)


def deliveries(order_id):
    return {
        "orderId": order_id,
        "description": faker.words(faker.random.randint(0, 15)),
        "dateTime": faker.date_this_month()
    }


def fail(delivery_id):
    return {
        "id": delivery_id,
        "reason": faker.words(faker.random.randint(0, 15))
    }


def registrations(delivery_id):
    return {
        "id": delivery_id,
        "description": faker.words(faker.random.randint(0, 15)),
        "dateTime": faker.date_this_month()
    }