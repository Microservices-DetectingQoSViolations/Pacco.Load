from faker import Faker
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def fake_collection(collection):
    times = faker.random.randint(1, len(collection) - 1)
    return list(set([faker.word(ext_word_list=collection) for _ in range(times)]))
