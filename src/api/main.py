from fastapi import FastAPI
from celery import Celery


celery_app = Celery(
    'api_celery',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

app = FastAPI()


@app.post('/submit')
def submit(img1: str, img2: str) -> int:
    """
    Submit two images to be compared. The images are put into the message
    queue, and the id corresponding to the task is returned.
    """
    return celery_app.send_task('models.similarity', kwargs={'img1': img1, 'img2': img2}).id


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