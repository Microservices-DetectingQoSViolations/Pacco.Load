from faker import Faker
from fake.predefined_fake_data import tags, parcel_sizes
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])


def create_parcel():
    return {
        "variant": faker.word(ext_word_list=tags),
        "size": faker.word(ext_word_list=parcel_sizes),
        "name": faker.name(),
        "description": faker.sentence(ext_word_list=tags)
    }
