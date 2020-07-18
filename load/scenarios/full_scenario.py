from locust import SequentialTaskSet, between, task
from fake import identity, customer, parcels
from json import dumps
from settings import httpSettings, add_auth
from http.on_response_actions import get_access_token, get_resource_id


class FullScenario(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''

        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.customer_data = customer.create_customer()

        self.parcel_data = parcels.create_parcel()
        self.parcel_id = ''

        self.order_id = ''

    def on_start(self):
        self.client.post("/identity/sign-up", dumps(self.user_data), headers=httpSettings['content_header'])

    @task
    def sing_in(self):
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = get_access_token

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

    @task
    def add_parcel(self):
        with self.client.post("/parcels", dumps(self.parcel_data),
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.parcel_id = get_resource_id

    @task
    def get_parcels(self):
        self.client.get("/parcels", headers=add_auth({}, self.access_token))

    @task
    def get_parcels_volume(self):
        self.client.get(f"/parcels/volume?parcelIds={dumps([self.parcel_id])}", headers=add_auth({}, self.access_token),
                        name="/parcels/volume")

    @task
    def create_order(self):
        with self.client.post("/orders", headers=add_auth({}, self.access_token)) as response:
            self.order_id = get_resource_id(response)



