from fastapi import HTTPException, Request, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status


class AuthBearer(HTTPBearer):
    """Обертка для аутентификации HTTP"""

    async def __call__(self, request: Request) -> str | None:
        try:
            credentials: HTTPAuthorizationCredentials = await super().__call__(request)
            return credentials.credentials  # Возвращаем Bearer токен
        except HTTPException as ex:
            if ex.status_code == status.HTTP_403_FORBIDDEN:
                return None  # Если токена нет, возвращаем None
            raise


class WebSocketAuthBearer:
    async def verify_token(self, websocket: WebSocket) -> str | None:
        """
        Проверяет JWT-токен из WebSocket.
        1️⃣ Токен может передаваться в `query_params` (?token=...)
        2️⃣ Токен может передаваться в `Authorization: Bearer ...`
        """
        token = websocket.query_params.get("token")  # Получаем токен из query
        if not token:
            auth_header = websocket.headers.get("Authorization")  # Ищем в заголовках
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]

        if not token:
            return None  # Если токена нет, возвращаем None

        return token


class AuthWrapper:
    """Обертка для аутентификации HTTP и WebSockets"""

    def __init__(self):
        self.http_auth = AuthBearer()
        self.ws_auth = WebSocketAuthBearer()

    async def __call__(
        self, request: Request = None, websocket: WebSocket = None
    ) -> str | None:
        """
        Определяет тип запроса и вызывает нужную аутентификацию.
        """
        if request:
            return await self.http_auth(request)  # Проверяем HTTP-запрос
        elif websocket:
            return await self.ws_auth.verify_token(websocket)  # Проверяем WebSocket
