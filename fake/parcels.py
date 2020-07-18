from faker import Faker
from fake.predefined_fake_data import tags, parcel_sizes

faker = Faker()
Faker.seed(7)


def create_parcel():
    return {
        "variant": faker.word(ext_word_list=tags),
        "size": faker.word(ext_word_list=parcel_sizes),
        "name": faker.name(),
        "description": faker.sentence(ext_word_list=tags)
    }
