"""
Simple functions to abstract the sending and receiving of websocket messages
via redis PubSub
"""
# stdlib imports
import os

# third-party imports
import redis


def _get_client(redis_host='localhost'):

    try:
        return redis.StrictRedis.from_url(os.environ['REDISCLOUD_URL'])
    except KeyError:
        return redis.StrictRedis(redis_host)


def _get_pubsub(redis_client):
    return redis_client.pubsub()


def publish(channel, message):
    redis_client = _get_client()
    redis_client.publish(channel, message)


def subscribe(channel, callback):
    redis_client = _get_client()
    redis_pubsub = _get_pubsub(redis_client)
    redis_pubsub.subscribe(channel)
    while True:
        for msg in redis_pubsub.listen():
            yield callback(msg)
