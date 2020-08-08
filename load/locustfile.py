from locust import between, HttpUser
from load.scenarios.basic_user import BasicUserSection
from load.scenarios.parcel_spammer import ParcelSpammer
from load.scenarios.vehicle_spammer import VehicleSpammer
from load.scenarios.full_scenario import FullScenario


class BasicSpammerUser(HttpUser):
    wait_time = between(0.8, 1.2)
    tasks = [BasicUserSection]


class ParcelSpammerUser(HttpUser):
    wait_time = between(0.8, 1.2)
    tasks = [ParcelSpammer]


class VehicleSpammerUser(HttpUser):
    wait_time = between(0.8, 1.2)
    tasks = [VehicleSpammer]


class FullScenarioUser(HttpUser):
    wait_time = between(1., 1.5)
    tasks = [FullScenario]
