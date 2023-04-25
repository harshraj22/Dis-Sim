import requests

url = "http://data_population:8020/healthcheck"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    # The request failed, so exit with a non-zero code to indicate failure
    exit(1)