from locust import SequentialTaskSet, between, task, HttpUser
from load.scenarios.new_users import NewUserSection, NewCustomerSection


class NewUser(HttpUser):
    wait_time = between(0.5, 0.8)
    tasks = [NewUserSection]


class NewCustomer(HttpUser):
    wait_time = between(0.5, 0.8)
    tasks = [NewCustomerSection]

