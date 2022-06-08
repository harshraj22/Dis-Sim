from celery import Celery
from time import sleep
import base64

app = Celery(
    'models',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)


@app.task()
def similarity(img1, img2):
    """Mock the similarity function between two images."""
    img1 = base64.b64decode(img1)
    img2 = base64.b64decode(img2)
    print(f'Similarity recieved args of type: {type(img1)}, {type(img2)}')
    sleep(10)
    return 1.0