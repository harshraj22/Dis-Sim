from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
import mysql.connector
from schemas import AuthDetails


app = FastAPI()


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
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    user_record = cursor_object.execute(f"""SELECT * FROM subscription_details where username = '{auth_details.username}'""")
    user_record = cursor_object.fetchall()
    # print(cursor_object.execute(f"""SELECT * FROM subscription_details""").fetchall())
    
    if len(user_record) > 0:
        user = {
            'username': user_record[0][0],
            'password': user_record[0][1]
        }

    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


# @app.get('/unprotected')
# def unprotected():
#     return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }