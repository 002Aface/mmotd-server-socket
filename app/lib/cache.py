"""
Simple redis cache
"""
# stdlib imports
import json
import os

# third-party imports
import redis


def _get_client(redis_host='localhost'):
    try:
        return redis.StrictRedis.from_url(os.environ['REDISCLOUD_URL'])
    except KeyError:
        return redis.StrictRedis(redis_host)

def get(name):
    """Retrieve the key `name` from cache or None if not found
    """
    client = _get_client()
    result = client.get(name)
    if result is not None:
        return json.loads(result)


def set(name, value, seconds=None):
    client = _get_client()
    client.set(name, json.dumps(value))
