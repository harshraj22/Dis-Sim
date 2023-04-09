import logging
import numpy as np
import base64
import requests
from locust import HttpUser, task, between

API_URL = "http://0.0.0.0:8001/submit"
LOGIN_URL = "http://0.0.0.0:8019/login"
USERNAME = "test"
PASSWORD = "test"

logging.basicConfig(level=logging.INFO)

def get_auth_token():
    """
    Retrieves authentication token by sending a POST request to login API.

    Returns:
        str: Authentication token.
    """
    data = {'username': USERNAME, 'password': PASSWORD}
    response = requests.post(LOGIN_URL, json=data)
    response.raise_for_status()
    auth_token = response.json().get('token')
    logging.info(f'Status_code: {response.status_code}, auth token: {auth_token}')
    return auth_token

img = np.random.rand(256, 256, 3)
img = base64.b64encode(img).decode("utf-8")

logging.info(f"curl -X POST -H 'Content-Type: application/json' -d '{{'username': '{USERNAME}', 'password': '{PASSWORD}'}}' {LOGIN_URL}")
auth_token = get_auth_token()

headers = {'User-Agent': 'Mozilla/5.0', 'Authorization': f'Bearer {auth_token}'}
payload = {'img1': img, 'img2': img}

def sync_health_check():
    """
    Sends a POST request to the API endpoint to perform a health check.
    """
    session = requests.Session()
    response = session.post(API_URL, headers=headers, files=payload)
    logging.info(f'Server responded with {response}')

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def check_api_endpoint(self):
        """
        Sends a POST request to the API endpoint using Locust client.
        """
        self.client.post("/submit", headers=headers, files=payload)
