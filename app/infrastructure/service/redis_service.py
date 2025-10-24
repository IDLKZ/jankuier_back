from datetime import timedelta

from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import get_redis_client


class RedisService:
    def __init__(self):
        self.redis_client = get_redis_client()

    def set_sota_token(self, name: str, value: str) -> None:
        """
        Сохраняет SOTA токен в Redis с TTL.

        Args:
            name: Ключ для хранения токена
            value: Значение токена
        """
        # Конвертируем минуты в секунды для консистентности с другими Redis операциями
        ttl_seconds = app_config.sota_token_save_minutes * 60
        self.redis_client.setex(name=name, time=ttl_seconds, value=value)

    def get_sota_token(self, name: str) -> str | None:
        """
        Получает SOTA токен из Redis.

        Args:
            name: Ключ токена

        Returns:
            str | None: Токен или None если не найден
        """
        return self.redis_client.get(name=name)
