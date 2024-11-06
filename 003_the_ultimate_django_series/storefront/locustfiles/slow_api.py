from locust import HttpUser, task, between


class SlowAPI(HttpUser):
    wait_time = between(1, 5)

    @task
    def slow_api(self):
        self.client.get("/playground/slow_endpoint/")
