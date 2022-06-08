from celery import Celery
import base64
from skimage.metrics import structural_similarity
import cv2
import numpy as np

app = Celery(
    'models',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)


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
    
    return round(score, 3)