# Script to populate data into redis from MySql
import redis
import mysql.connector
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
  

database = mysql.connector.connect(
  host ="subscription_db",
  user ="root",
  passwd ="mypassword",
  database = 'DB'
)

r = redis.StrictRedis(host='redis', port=6379, decode_responses=True, password="")
ALLOWED_PREFIX = 'allowed' # max number of requests allowed per WINDOW_LENGTH

# preparing a cursor object
cursor_object = database.cursor()
user_record = """SELECT * FROM subscription """
records = cursor_object.execute(user_record)
result = cursor_object.fetchall()

# >>> print(result)
# [(1, 'test', 'Free', 2), (2, 'premium', 'Advanced', 200)]
  
print(result) # ToDo: Change this to logger
database.close()

for id, username, subscription_tier, request_limit in result:
  r.set(f'{ALLOWED_PREFIX}-{username}', request_limit)

r.close()
