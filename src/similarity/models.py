from celery import Celery
import base64
from skimage.metrics import structural_similarity
import cv2
import numpy as np
from time import sleep
import os

app = Celery(
    'models',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

redis_slave_urls = os.environ.get('REDIS_SLAVE_URLS', 'redis://localhost:6379/0').split(',')
# REDIS_SLAVE_URLS=redis://slave1:6379,redis://slave2:6379,redis://slave3:6379

result_backend_transport_options = {
    'visibility_timeout': 3600,
    'fanout_prefix': True,
    'fanout_patterns': True,
    'fanout_routing_key_prefix': True,
    'fanout_deliver': True,
    'fanout_cycle': True,
    'fanout_queue_ttl': 300,
    'fanout_add_new_consumers': True,
    'fanout_wait_for_consumers': True,
    'fanout_update_routing': True,
    'fanout_delete_queues': True,
    'fanout_ttl': 600,
    'fanout_retry': True,
    'fanout_transport_options': {
        'master': 'redis://localhost:6379/0',
        'slaves': redis_slave_urls
    }
}

app.conf.update(
    result_backend='redis',
    result_backend_transport_options=result_backend_transport_options
)

# frequency with which Celery checks for changes in environment variables
app.conf.beat_max_loop_interval = 60

@app.task()
def similarity(img1, img2) -> float:
    """Uses Structural Similarity to compare two images. For real applications,
    more advanced image comparison techniques should be used. eg. https://github.com/serengil/deepface
    However, for demo purposes, this is sufficient. """

    # Images are sent as base64 strings. Decode them back to bytes.
    img1 = base64.b64decode(img1)
    img2 = base64.b64decode(img2)
    
    # https://stackoverflow.com/a/17170855/10127204
    img1 = np.fromstring(img1, np.uint8)
    img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    img1 = cv2.resize(img1, (300, 300))

    img2 = np.fromstring(img2, np.uint8)
    img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    img2 = cv2.resize(img2, (300, 300))

    # Convert images to grayscale
    first_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)

    # sleep(10)
    
    return round(score, 3)
