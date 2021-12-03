import redis
from typing import Any

class Redis:
    def __init__(self):
        redis_host = "redis"
        redis_port = 6379
        redis_password = ""
        self.client = redis.StrictRedis(
            host=redis_host, 
            port=redis_port, 
            password=redis_password, 
            decode_responses=True)

    def set(self, key: str, value: Any):
        self.client.set(key, value)

    def get(self, key: str):
        return self.client.get(key)