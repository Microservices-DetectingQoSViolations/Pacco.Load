from faker import Faker

Faker.seed(1)
faker = Faker()


def sign_up():
    return {
        "email": faker.ascii_safe_email(),
        "password": faker.password(),
        "role": "user"
    }


def sign_in_valid(email, password):
    return {
        "email": faker.ascii_safe_email(),
        "password": faker.password()
    }


def sign_in_invalid(password):
    invalid = faker.password()
    while invalid == password:
        invalid = faker.password()
    return {
        "email": faker.ascii_safe_email(),
        "password": invalid
    }

