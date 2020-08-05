from locust import task
from fake import identity, customer, parcels
from json import dumps
from settings import httpSettings, add_auth
from http_utils.on_response_actions import get_resource_id
from load.scenarios.basic_user import BasicUserSection


class ParcelSpammer(BasicUserSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''

        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.customer_data = customer.create_customer()

        self.parcel_ids = []

        self.order_id = ''

    def on_start(self):
        super().on_start()
        self.add_parcel()
        self.add_parcel()

    @task(5)
    def add_parcel(self):
        with self.client.post("/parcels", dumps(parcels.create_parcel()),
                              headers=add_auth(httpSettings['content_header'], self.access_token),
                              name="/parcels") as response:
            self.parcel_ids.append(get_resource_id(response))

    @task(5)
    def get_parcels(self):
        self.client.get("/parcels",
                        headers=add_auth({}, self.access_token),
                        name="/parcels")

    @task(5)
    def get_parcel(self):
        self.client.get(f"/parcels/{parcels.any_parcel(self.parcel_ids)}",
                        headers=add_auth({}, self.access_token),
                        name="/parcel")

    @task(5)
    def get_parcels_volume(self):
        self.client.get(f"/parcels/volume?parcelIds={dumps([parcels.any_parcel(self.parcel_ids)])}",
                        headers=add_auth({}, self.access_token),
                        name="/parcels/volume")

    @task(1)
    def create_order(self):
        with self.client.post("/orders", dumps({}),
                              headers=add_auth(httpSettings['content_header'], self.access_token),
                              name="/orders") as response:
            self.order_id = get_resource_id(response)

    @task(1)
    def get_orders(self):
        self.client.get("/orders",
                        headers=add_auth({}, self.access_token),
                        name="/orders")
