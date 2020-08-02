from locust import TaskSet, task
from fake import identity, customer
from json import dumps
from settings import httpSettings, add_auth
from http_utils.on_response_actions import get_access_token


class BasicUserSection(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''
        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.customer_data = customer.create_customer()

    def on_start(self):
        self.client.post("/identity/sign-up", dumps(self.user_data), headers=httpSettings['content_header'])
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = get_access_token(response)
            self.client.get("/identity/me", headers=add_auth({}, self.access_token))
            self.client.post("/customers", dumps(self.customer_data),
                             headers=add_auth(httpSettings['content_header'], self.access_token))

    @task(2)
    def sing_in(self):
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = get_access_token(response)

    @task(1)
    def identity_me(self):
        self.client.get("/identity/me", headers=add_auth({}, self.access_token))

    @task(1)
    def customer_data(self):
        self.client.get("/customers/me", headers=add_auth({}, self.access_token))