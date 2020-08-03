from locust import between, HttpUser
from load.scenarios.fun_with_parcels import FunWithParcels
from load.scenarios.fun_with_vehicles import FunWithVehicles
from load.scenarios.full_scenario import FullScenario


class ParcelUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [FunWithParcels]


class VehicleUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [FunWithVehicles]


class FullScenarioUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [FullScenario]
