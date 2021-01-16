from locust import between, HttpUser
from load.scenarios.basic_user import BasicUserSection
from load.scenarios.parcel_spammer import ParcelSpammer
from load.scenarios.vehicle_spammer import VehicleSpammer
from load.scenarios.full_scenario import FullScenario
from locust import LoadTestShape
from locust.env import Environment
from locust.log import setup_logging

import numpy as np
import random
import time


setup_logging("INFO", None)
iters = 42
run_times = []

for iter in range(iters):
    class BasicSpammerUser(HttpUser):
        wait_time = between(1.2, 1.6)
        tasks = [BasicUserSection]


    class ParcelSpammerUser(HttpUser):
        wait_time = between(1.2, 1.6)
        tasks = [ParcelSpammer]


    class VehicleSpammerUser(HttpUser):
        wait_time = between(1.2, 1.6)
        tasks = [VehicleSpammer]


    class FullScenarioUser(HttpUser):
        wait_time = between(1.5, 2.3)
        tasks = [FullScenario]


    env = Environment(user_classes=[ParcelSpammerUser, VehicleSpammerUser, FullScenarioUser],
                      host='http://192.168.0.220:32120', reset_stats=True)
    env.create_local_runner()

    start = time.time()


    class StagesShape(LoadTestShape):
        stages_len = random.randint(8, 18)

        step = int(420 / stages_len)

        stages_time = np.linspace(step, 420, stages_len)
        stages = []
        users = 15
        spawn_rate = 0
        for st in stages_time:
            users = users + random.randint(6, 15)
            spawn_rate = random.randint(1, 3)
            stages.append({'duration': int(st), 'users': users, 'spawn_rate': spawn_rate})

        def tick(self):
            run_time = self.get_run_time()

            for stage in self.stages:
                if run_time < stage["duration"]:
                    tick_data = (stage["users"], stage["spawn_rate"])
                    return tick_data
            return None
    stages_shape = StagesShape()
    stages_shape.reset_time()
    env.runner.start_shape(stages_shape)

    # in 420 seconds stop the runner
    time.sleep(420)

    env.runner.quit()

    stop = time.time()
    with open('../testdata/spam9.txt', 'a') as spam_data:
        spam_data.write(f'{stop}, ')

    time.sleep(180)
    env = None
