from locust import SequentialTaskSet, between, task, HttpUser
from fake import identity, customer
from json import dumps
from settings import httpSettings, add_auth


class NewUserSection(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.access_token = ''

    def on_start(self):
        self.client.post("/identity/sign-up", dumps(self.user_data), headers=httpSettings['content_header'])

    @task
    def sing_in(self):
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = response.json()['accessToken']

    @task
    def identity_me(self):
        self.client.get("/identity/me", headers=add_auth({}, self.access_token))


class NewCustomerSection(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''
        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.customer_data = customer.create_customer()

    def on_start(self):
        self.client.post("/identity/sign-up", dumps(self.user_data), headers=httpSettings['content_header'])

    @task
    def sing_in(self):
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = response.json()['accessToken']

    @task
    def identity_me(self):
        self.client.get("/identity/me", headers=add_auth({}, self.access_token))

    @task
    def complete_customer(self):
        self.client.post("/customers", dumps(self.customer_data),
                         headers=add_auth(httpSettings['content_header'], self.access_token))

    @task
    def customer_data(self):
        self.client.get("/customers/me", headers=add_auth({}, self.access_token))


class NewUser(HttpUser):
    wait_time = between(0.5, 0.8)
    tasks = [NewUserSection]


class NewCustomer(HttpUser):
    wait_time = between(0.5, 0.8)
    tasks = [NewCustomerSection]