from celery import Celery
from time import sleep

app = Celery(
    'models',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)


@app.task()
def similarity(img1, img2):
    """Mock the similarity function between two images."""
    sleep(5)
    return 1.0