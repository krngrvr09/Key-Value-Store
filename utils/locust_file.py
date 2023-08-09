from locust import HttpUser, task
import random

f = open("./shuffled_1m_example.data")
lines = f.readlines()
f.close()
lines = [i.strip() for i in lines]

class MyUser(HttpUser):
    @task
    def my_task(self):
        custom_param_value = lines[random.randint(0,len(lines))]
        response = self.client.get(f"/?key={custom_param_value}")
        print(f"Response: {response.text}")

