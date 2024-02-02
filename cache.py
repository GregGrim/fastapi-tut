from datetime import timedelta

import redis

from constants import ACCESS_TOKEN_EXPIRE_MINUTES

r_db = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def add_token(token: str, user_id: int):
    key = get_auth_redis_key(user_id, token)
    r_db.set(key, 1)
    r_db.expire(key, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def get_auth_redis_key(user_id: int, token: str) -> str:
    return f"auth:{user_id}:{token}"


def token_exists(token: str, user_id: int) -> bool:
    return r_db.exists(get_auth_redis_key(user_id, token))
