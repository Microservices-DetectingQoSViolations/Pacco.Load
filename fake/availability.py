from faker import Faker

faker = Faker()
faker.seed(4231)

tags = ['risk', 'risk1', 'glass', 'wine', 'oil', 'diesel', 'gasoline', 'chocolate', 'fruits',
        'fruits1', 'fruits2', 'vehicle', 'armor', 'armor1', 'armor2', 'gun', 'gun1', 'gun2']


def resources(resource_id):
    res_tags = []
    rand_val = faker.random.random()

    res_tags.append(tags[faker.random.randint(0, len(tags) - 1)])
    if rand_val > 0.95:
        res_tags.append(tags[faker.random.randint(0, len(tags) - 1)])
    if rand_val > 0.99:
        res_tags.append(tags[faker.random.randint(0, len(tags) - 1)])

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
