from locust import between, HttpUser
from load.scenarios.parcel_spammer import ParcelSpammer
from load.scenarios.vehicle_spammer import VehicleSpammer
from load.scenarios.full_scenario import FullScenario


class ParcelSpammerUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [ParcelSpammer]


class VehicleSpammerUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [VehicleSpammer]


class FullScenarioUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [FullScenario]
