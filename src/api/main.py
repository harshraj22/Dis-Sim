from fastapi import Depends, FastAPI, Form, UploadFile
from celery import Celery
import base64
import json

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from kafka import KafkaProducer

celery_app = Celery(
    'api_celery',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

KAFKA_TOPIC = 'DATA_MONITOR'

app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers='broker:29092',
    api_version=(2, 0, 2) # https://stackoverflow.com/a/56449512/10127204
    )

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret = 'SECRET'

def decode_token(token):
    print(f'Token Recieved: {token}')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')

def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


@app.post('/healthcheck')
def healthcheck(user_id = Depends(auth_wrapper)):
    return {'user_id': user_id}


@app.post('/submit')
async def submit(img1: UploadFile = UploadFile(filename='img1'), img2: UploadFile = UploadFile(filename='img2'), user_id = Depends(auth_wrapper)) -> str:
    """
    Submit two images to be compared. The images are put into the message
    queue, and the id corresponding to the task is returned.

    Note: One can only send JSON objects from Fastapi. So, the images are
    encoded as base64 strings. On the Celery side, the images are decoded
    back to bytes.
    """
    # shutil.copyfileobj(img1.file, open(img1.filename, 'wb'))
    img1_contents = await img1.read()
    img2_contents = await img2.read()
    data = {
            "img1": base64.b64encode(img1_contents).decode("utf-8"),
            "img2": base64.b64encode(img2_contents).decode("utf-8"),
        }

    print(f'Sending data to kafka: {data.keys()}')
    producer.send(KAFKA_TOPIC, json.dumps(data).encode("utf-8"))

    return celery_app.send_task(
        "models.similarity",
        kwargs=data,
    ).id


@app.get('/status/{task_id}')
def status(task_id: str) -> str:
    """ Check the status of a task. """
    return str(celery_app.AsyncResult(task_id).state)


@app.get('/result/{task_id}')
def result(task_id: str) -> float:
    """ Get the result of a task. """
    return celery_app.AsyncResult(task_id).result

