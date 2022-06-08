from fastapi import FastAPI, Form, UploadFile
from celery import Celery
import base64


celery_app = Celery(
    'api_celery',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

app = FastAPI()


@app.post('/submit')
def submit(img1: UploadFile = Form(), img2: UploadFile = Form()) -> str:
    """
    Submit two images to be compared. The images are put into the message
    queue, and the id corresponding to the task is returned.

    Note: One can only send JSON objects from Fastapi. So, the images are
    encoded as base64 strings. On the Celery side, the images are decoded
    back to bytes.
    """
    # shutil.copyfileobj(img1.file, open(img1.filename, 'wb'))
    # print(f'written to {img1.filename}')
    img1_contents = img1.file.read()
    img2_contents = img2.file.read()
    return celery_app.send_task(
        "models.similarity",
        kwargs={
            "img1": base64.b64encode(img1_contents).decode("utf-8"),
            "img2": base64.b64encode(img2_contents).decode("utf-8"),
        },
    ).id


@app.get('/status/{task_id}')
def status(task_id: str) -> str:
    """
    Check the status of a task.
    """
    return str(celery_app.AsyncResult(task_id).state)


@app.get('/result/{task_id}')
def result(task_id: str) -> float:
    """
    Get the result of a task.
    """
    return celery_app.AsyncResult(task_id).result

""" 
# https://stackoverflow.com/questions/7172784/how-do-i-post-json-data-with-curl
curl -X POST \
http://localhost:8001/submit \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"img1": "bar",
"img2": "ipsum"
}'
"""