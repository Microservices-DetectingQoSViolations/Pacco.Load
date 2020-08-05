from locust import task
from fake import identity, customer, vehicles
from json import dumps
from settings import httpSettings, add_auth
from http_utils.on_response_actions import get_resource_id
from load.scenarios.basic_user import BasicUserSection


class VehicleSpammer(BasicUserSection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = ''

        self.user_data = identity.sign_up()
        self.login_data = {i: self.user_data[i] for i in self.user_data if i != 'role'}
        self.customer_data = customer.create_customer()

        self.vehicle_ids = []

    def on_start(self):
        super().on_start()
        self.add_vehicle()
        self.add_vehicle()

    @task(5)
    def add_vehicle(self):
        with self.client.post("/vehicles", dumps(vehicles.create_vehicle()),
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.vehicle_ids.append(get_resource_id(response))

    @task(5)
    def get_vehicle(self):
        self.client.get(f"/vehicles/{vehicles.any_vehicle(self.vehicle_ids)}",
                        headers=add_auth({}, self.access_token),
                        name="/vehicle")

    @task(5)
    def browse_vehicle(self):
        cap, var = vehicles.browse_vehicle()
        self.client.get(f"/vehicles?payloadCapacity={cap}&loadingCapacity={cap}&variants={var}",
                        headers=add_auth({}, self.access_token),
                        name="/vehicles?browse")
