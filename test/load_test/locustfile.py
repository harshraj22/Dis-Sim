import time
from locust import HttpUser, task, between
import requests

# wget https://imageio.forbes.com/specials-images/imageserve/5db4c7b464b49a0007e9dfac/Photo-of-Maltese-dog/960x0.jpg
with open('../../artifacts/960x0.jpg', 'rb') as f:
    img = f.read()

headers = {'User-Agent': 'Mozilla/5.0'}
paylod = {'img1': img, 'img2': img}

def sync_health_check():
    session = requests.Session()
    response = session.post('http://0.0.0.0:8001/submit', headers=headers, files=paylod)
    print(f'Server responded with {response}')


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def check_api_endpoint(self):
        self.client.post("/submit", headers=headers, files={'img1': img, 'img2': img})


