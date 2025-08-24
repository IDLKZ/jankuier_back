from datetime import timedelta

from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import get_redis_client


class RedisService:
    def __init__(self):
        self.redis_client = get_redis_client()


    def set_sota_token(self,name:str,value:str):
        self.redis_client.setex(name=name,time=timedelta(minutes=app_config.sota_token_save_minutes),value=value)

    def get_sota_token(self,name:str)->str:
        return self.redis_client.get(name=name)
