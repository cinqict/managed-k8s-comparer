from locust import HttpUser, task, between
import random

class DummyAppUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def health(self):
        self.client.get("/health")

    @task(2)
    def write(self):
        self.client.post("/write", json={"content": "Hello from Locust!"})

    @task(2)
    def read(self):
        self.client.get("/read")

    @task(1)
    def compute(self):
        iterations = random.randint(100, 1000000)
        self.client.get(f"/compute?iterations={iterations}")