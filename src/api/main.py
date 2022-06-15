from fastapi import Depends, FastAPI, Form, UploadFile
from celery import Celery
import base64

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

celery_app = Celery(
    'api_celery',
    backend='redis://redis:6379/0',
    broker='redis://redis:6379/0'
)

app = FastAPI()

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
    return celery_app.send_task(
        "models.similarity",
        kwargs={
            "img1": base64.b64encode(img1_contents).decode("utf-8"),
            "img2": base64.b64encode(img2_contents).decode("utf-8"),
        },
    ).id


@app.get('/status/{task_id}')
def status(task_id: str) -> str:
    """ Check the status of a task. """
    return str(celery_app.AsyncResult(task_id).state)


@app.get('/result/{task_id}')
def result(task_id: str) -> float:
    """ Get the result of a task. """
    return celery_app.AsyncResult(task_id).result

