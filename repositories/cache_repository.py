import redis
from datetime import timedelta

from entities import settings


def get_auth_redis_key(user_id: int, token: str) -> str:
    return f"auth:{user_id}:{token}"


class CacheRepository:
    def __init__(self) -> None:
        self.r_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

    def add_token(self, token: str, user_id: int):
        key = get_auth_redis_key(user_id, token)
        self.r_db.set(key, 1)
        self.r_db.expire(key, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    def token_exists(self, token: str, user_id: int) -> bool:
        return self.r_db.exists(get_auth_redis_key(user_id, token))

    def remove_token(self, token: str):
        keys_to_delete = self.r_db.keys(f"auth:*:{token}")
        for key in keys_to_delete:
            self.r_db.delete(key)

    def remove_all_user_tokens(self, user_id: int):
        keys_to_delete = self.r_db.keys(f"auth:{user_id}:*")
        for key in keys_to_delete:
            self.r_db.delete(key)
