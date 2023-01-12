

# docker run -p 6379:6379 --name redis_server redis:4-alpine
import logging
import redis
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


r = redis.StrictRedis(host='redis', port=6379, decode_responses=True, password="")

WINDOW_LENGTH = 15 # 86400 # 24 hours in Seconds
ALLOWED_PREFIX = 'allowed' # max number of requests allowed per WINDOW_LENGTH
REQUESTED_PREFIX = 'requested' # number of requests the user has made till now


def get_total_allwed_request(username: str):
    """Returns the total allowed request corresponding to the given user. Assumes
    the redis cache is always updated/in-sync with the mysql db (Payment microservice
    is expected to keep it updated.
    
    Raises ValueError in case the value corresponding to authenticated user is
    not found in the cache. """

    total_allowed_req = r.get(f'{ALLOWED_PREFIX}-{username}')
    if total_allowed_req is None:
        raise ValueError(f'Total Allowed Request for user {username} does not exist in Redis Cache')
    return int(total_allowed_req)


def expire_old_requests(username: str):
    """Given the username, expires all the old requests that are not useful
    while calculating the current rate limit. """
    p = r.pipeline()
    p.zremrangebyscore(f'{REQUESTED_PREFIX}-{username}', 0, time.time() - WINDOW_LENGTH)
    p.expire(f'{REQUESTED_PREFIX}-{username}', WINDOW_LENGTH)
    p.execute()


def add_request(username: str):
    """Adds current request to the cache"""
    cur_time = time.time()
    r.zadd(f'{REQUESTED_PREFIX}-{username}', {cur_time: cur_time})
    logger.info(f'Added Request entry in Redis cache for user: {username} at {cur_time}')


def get_active_request_count(username: str):
    """Returns the total number of active request that the user had made in the
    defined window length from current time."""
    return len(r.zrange(f'{REQUESTED_PREFIX}-{username}', 0, -1))


def is_allowed(username: str):
    """Checks (and returns) if current user is allowed to make more requests
    based on their request history and subscription tier."""
    expire_old_requests(username)
    total_allowed_req = get_total_allwed_request(username)
    active_req = get_active_request_count(username)
    logger.info(f'for user: {username}, total_allowed: {total_allowed_req}, active: {active_req}')
    if total_allowed_req >= active_req + 1:
        add_request(username)
        return True
    return False

