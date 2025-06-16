from locust import HttpUser, task, between

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
        self.client.get("/compute?iterations=1000")