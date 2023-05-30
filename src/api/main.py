from fastapi import Depends, FastAPI, Form, UploadFile
from celery import Celery
import base64
import json
import logging
import os
from pydantic import BaseModel

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from kafka import KafkaProducer

from subscription_rate_limiter.rate_limiter import is_allowed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# redis_slave_urls = os.environ.get('REDIS_SLAVE_URLS', 'redis://redis_slave:6379/0').split(',')

celery_similarity = Celery(
    'api_celery',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

celery_feedback = Celery(
    'feedback_celery',
    backend='redis://redis:6379/1',
    broker='redis://redis:6379/1'
)

# celery_app.conf.update(
#     result_backend=','.join(redis_slave_urls),
# )


KAFKA_TOPIC = 'DATA_MONITOR'

app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers='broker:29092',
    api_version=(2, 0, 2) # https://stackoverflow.com/a/56449512/10127204
    )

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = 'SECRET'

class Feedback(BaseModel):
    task_id: str
    response: bool

def decode_token(token):
    logger.info(f'Token Recieved: {token}')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


@app.get('/healthcheck', status_code=200)
def healthcheck():
    return {'status': 'healthy'}


@app.post('/submit')
async def submit(img1: UploadFile = UploadFile(filename='img1'), img2: UploadFile = UploadFile(filename='img2'), user_id = Depends(auth_wrapper)) -> str:
    """
    Submit two images to be compared. The images are put into the message
    queue, and the id corresponding to the task is returned.

    Note: One can only send JSON objects from Fastapi. So, the images are
    encoded as base64 strings. On the Celery side, the images are decoded
    back to bytes.
    """
    logger.info(f'user_id {user_id} submitted a post request.')

    if not is_allowed(user_id):
        raise HTTPException(status_code=403, detail='Rate Limit Exceeded')
    # shutil.copyfileobj(img1.file, open(img1.filename, 'wb'))
    img1_contents = await img1.read()
    img2_contents = await img2.read()
    data = {
            "img1": base64.b64encode(img1_contents).decode("utf-8"),
            "img2": base64.b64encode(img2_contents).decode("utf-8"),
        }

    logger.info(f'Sending data to kafka: {data.keys()}')
    producer.send(KAFKA_TOPIC, json.dumps(data).encode("utf-8"))

    return celery_similarity.send_task(
        "models.similarity",
        kwargs=data,
    ).id


@app.get('/status/{task_id}')
def status(task_id: str) -> str:
    """ Check the status of a task. """
    return str(celery_similarity.AsyncResult(task_id).state)


@app.get('/result/{task_id}')
def result(task_id: str) -> float:
    """ Get the result of a task. """
    return celery_similarity.AsyncResult(task_id).result

@app.post('/feedback')
def feedback(feedback: Feedback, status_code=200):
    logger.info(f'Submitting feedback for task: {feedback.task_id} as: {feedback.response}')
    return celery_feedback.send_task(
        "feedback.feedback",
        kwargs={'task_id': feedback.task_id, 'response': feedback.response},
    ).id

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)