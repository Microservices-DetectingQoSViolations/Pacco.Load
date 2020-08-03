from locust import SequentialTaskSet, task
from fake import availability, deliveries, identity, customer, parcels, vehicles, orders
from json import dumps
from settings import httpSettings, add_auth
from http_utils.on_response_actions import get_access_token, get_resource_id


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
        self.order_date = orders.fake_order_date()

        self.vehicle_id = ''

        self.delivery_id = ''

    def on_start(self):
        self.client.post("/identity/sign-up", dumps(self.user_data),
                         headers=httpSettings['content_header'])

    @task
    def sing_in(self):
        with self.client.post("/identity/sign-in", dumps(self.login_data),
                              headers=httpSettings['content_header']) as response:
            self.access_token = get_access_token(response)

    @task
    def identity_me(self):
        self.client.get("/identity/me",
                        headers=add_auth({}, self.access_token))

    @task
    def complete_customer(self):
        self.client.post("/customers", dumps(self.customer_data),
                         headers=add_auth(httpSettings['content_header'], self.access_token))

    @task
    def customer_data(self):
        self.client.get("/customers/me",
                        headers=add_auth({}, self.access_token))

    @task
    def add_parcel(self):
        with self.client.post("/parcels", dumps(self.parcel_data),
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.parcel_id = get_resource_id(response)

    @task
    def get_parcels(self):
        self.client.get("/parcels",
                        headers=add_auth({}, self.access_token))

    @task
    def get_parcels_volume(self):
        self.client.get(f"/parcels/volume?parcelIds={dumps([self.parcel_id])}",
                        headers=add_auth({}, self.access_token),
                        name="/parcels/volume")

    @task
    def create_order(self):
        with self.client.post("/orders", dumps({}),
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.order_id = get_resource_id(response)

    @task
    def get_orders(self):
        self.client.get("/orders",
                        headers=add_auth({}, self.access_token))

    @task
    def get_parcels(self):
        self.client.get(f"/orders/{self.order_id}/parcels/{self.parcel_id}",
                        headers=add_auth(httpSettings['content_header'], self.access_token),
                        name="/order/parcels")

    @task
    def get_order(self):
        self.client.get(f"/orders/{self.order_id}",
                        headers=add_auth({}, self.access_token),
                        name="/order")
        self.client.get(f"/orders/{self.order_id}",
                        headers=add_auth({}, self.access_token),
                        name="/order")

    @task
    def create_vehicle(self):
        with self.client.post(f"/vehicles",
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.vehicle_id = get_resource_id(response)

    @task
    def browse_vehicle(self):
        cap, var = vehicles.browse_vehicle()
        self.client.get(f"/vehicles?payloadCapacity={cap}&loadingCapacity={cap}&variants={var}",
                        headers=add_auth({}, self.access_token),
                        name="/vehicles?browse")

    @task
    def create_availability(self):
        self.client.post("/availability/resources", dumps(availability.resources(self.vehicle_id)),
                         headers=add_auth(httpSettings['content_header'], self.access_token))

    @task
    def browse_availability_by_tags(self):
        match_all, tags = availability.browse_tags_data(False)
        self.client.get(f"/resources?tags={dumps(tags)}&matchAllTags={match_all}",
                        headers=add_auth({}, self.access_token),
                        name="/resources?tags")

    @task
    def set_delivery_date(self):
        self.client.post(f"/orders/{self.order_id}/vehicles/{self.vehicle_id}", dumps(self.order_date),
                         headers=add_auth(httpSettings['content_header'], self.access_token),
                         name="/orders/vehicles")

    @task
    def make_reservation(self):
        self.client.post(f"/availability/resources/{self.vehicle_id}/reservations/{self.order_date}",
                         dumps(availability.get_priority()),
                         headers=add_auth(httpSettings['content_header'], self.access_token),
                         name="/availability/resources/reservations/date")

    @task
    def check_reservation(self):
        self.client.get(f"/availability/resources/{self.vehicle_id}",
                        headers=add_auth({}, self.access_token),
                        name="/availability/resources")

    @task
    def start_delivery(self):
        with self.client.post(f"/deliveries", dumps(deliveries.start_delivery(self.order_id, self.order_date)),
                              headers=add_auth(httpSettings['content_header'], self.access_token)) as response:
            self.delivery_id = get_resource_id(response)

    @task
    def fix_delivery(self):
        self.client.post(f"/deliveries/{self.delivery_id}/registrations",
                         dumps(deliveries.registrations(self.delivery_id, self.order_date)),
                         headers=add_auth(httpSettings['content_header'], self.access_token),
                         name="/deliveries/registrations")

    @task
    def complete_delivery(self):
        with self.client.post(f"/deliveries/{self.delivery_id}/complete", dumps(deliveries.complete(self.order_date)),
                              headers=add_auth(httpSettings['content_header'], self.access_token),
                              name="/deliveries/complete") as response:
            self.delivery_id = get_resource_id(response)

    @task
    def check_delivery(self):
        with self.client.get(f"/deliveries/{self.delivery_id}",
                             headers=add_auth({}, self.access_token),
                             name="/delivery") as response:
            self.delivery_id = get_resource_id(response)

    @task
    def get_order_after(self):
        self.client.get(f"/orders/{self.order_id}",
                        headers=add_auth({}, self.access_token),
                        name="/order")
