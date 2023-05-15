# Script to populate data into redis from MySql
import redis
import mysql.connector
import logging
from fastapi import FastAPI
from pydantic import BaseModel
import requests


class Username(BaseModel):
  username: str


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
  

app = FastAPI()

r = redis.StrictRedis(host='redis', port=6379, decode_responses=True, password="")
ALLOWED_PREFIX = 'allowed' # max number of requests allowed per WINDOW_LENGTH


@app.post('/sync', status_code=200)
def sync(username: Username):
  database = mysql.connector.connect(
    host ="subscription_db",
    user ="root",
    passwd ="mypassword",
    database = 'DB'
  )

  # preparing a cursor object
  cursor_object = database.cursor()

  print(f'Syncing {username} to redis')
  user_record = f"""SELECT * FROM subscription_details where username = '{username.username}'"""
  print('User Record:', user_record)
  cursor_object.execute(user_record)
  result = cursor_object.fetchall()

  for username, subscription_tier, request_limit, retention_period in result:
    r.set(f'{ALLOWED_PREFIX}-{username}', request_limit) 


  cursor_object.close()
  database.close()

@app.on_event("startup")
@app.get('/sync_all', status_code=200)
def sync_all():

  database = mysql.connector.connect(
    host ="subscription_db",
    user ="root",
    passwd ="mypassword",
    database = 'DB'
  )

  # preparing a cursor object
  cursor_object = database.cursor()

  user_record = """SELECT * FROM subscription_details """
  records = cursor_object.execute(user_record)
  result = cursor_object.fetchall()

  # >>> print(result)
  # [('free_user', 'Free', 10, 1), ('basic_user', 'Basic', 100, 15), ('advanced_user', 'Advanced', 1000, 60), ('test', 'Advanced', 1000, 60)]

  logger.info(result)

  for username, subscription_tier, request_limit, retention_period in result:
    r.set(f'{ALLOWED_PREFIX}-{username}', request_limit)

  cursor_object.close()
  database.close()

@app.get('/healthcheck', status_code=200)
def healthcheck():
  return 'OK'

# r.close()
if __name__ == '__main__':
  requests.get('http://data_population:8020/sync_all/')

