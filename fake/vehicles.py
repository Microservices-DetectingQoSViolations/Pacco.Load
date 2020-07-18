from faker_vehicle import VehicleProvider
from faker import Faker
from fake.predefined_fake_data import tags
from fake.settings import fake_settings

faker = Faker()
Faker.seed(fake_settings['seed'])
faker.add_provider(VehicleProvider)


def create_vehicle():
    make = faker.vehicle_make()
    model = faker.vehicle_model()
    cap = get_cap()
    price = (faker.random.random() + 1.0) * cap

    return {
      "brand": faker.vehicle_make(),
      "model": faker.vehicle_model(),
      "description": f"{make} {model} {faker.vehicle_category()}",
      "payloadCapacity": 1000 * cap,
      "loadingCapacity": 1000 * cap,
      "pricePerService": 10 * price,
      "variants": get_variant()
    }


def browse_vehicle():
    return get_cap(), get_variant()


def get_cap():
    return faker.random.randint(1, 15)


def get_variant():
    return faker.word(ext_word_list=tags)
