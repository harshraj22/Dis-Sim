from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
import mysql.connector
from schemas import AuthDetails
import logging
import requests


app = FastAPI()

logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
users = [{'username': 'test', 'password': auth_handler.get_password_hash('test')}]

database = mysql.connector.connect(
  host ="subscription_db",
  user ="root",
  passwd ="mypassword",
  database = 'DB'
)
cursor_object = database.cursor()

@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    cursor_object.execute(f"""SELECT * FROM auth where username = '{auth_details.username}'""")
    if len(cursor_object.fetchall()) > 0:
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    cursor_object.execute(f"""INSERT INTO auth VALUES ('{auth_details.username}', '{hashed_password}', 'Free')""")
    
    database.commit()
    response = requests.post(f'http://data_population:8020/sync/', json={'username': auth_details.username})
    print(f'Response from data_population for syncing data: {response.status_code}')

    logger.info(f"User {auth_details.username} registered successfully")
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    user_record = cursor_object.execute(f"""SELECT * FROM auth where username = '{auth_details.username}'""")
    user_record = cursor_object.fetchall()
    
    if len(user_record) > 0:
        user = {
            'username': user_record[0][0],
            'password': user_record[0][1]
        }

        logger.debug(f'Entered password: {auth_details.password}, saved password: {user["password"]}')
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    logger.info(f"User {auth_details.username} logged in successfully")
    return { 'token': token }


# @app.get('/unprotected')
# def unprotected():
#     return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    logger.info(f"User {username} accessed protected route")
    return { 'name': username }
