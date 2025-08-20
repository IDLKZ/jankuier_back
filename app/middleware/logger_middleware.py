import sys

from fastapi import Request
from jose import jwt
from loguru import logger
from datetime import datetime
import time
import json
from app.infrastructure.app_config import app_config

"""
Модуль логирования HTTP-запросов FastAPI с использованием Loguru.

Настраивает файловое и консольное логирование, сохраняет подробные сведения о каждом запросе,
включая тело, параметры, пользователя (если доступен JWT), время выполнения, путь и описание маршрута.
"""
logger.remove()
logger.add(
    app_config.logger_filepath,
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
    serialize=False,
    enqueue=True,
)
if app_config.logger_stdout:
    # Лог в stdout (консоль)
    logger.add(
        sink=sys.stdout,
        level=app_config.logger_level,
        serialize=app_config.logger_serializer,
        colorize=app_config.logger_colorize,
        enqueue=app_config.logger_enqueue,
        backtrace=app_config.logger_backtrace,
        diagnose=app_config.logger_diagnose,
    )


async def log_requests(request: Request, call_next):
    """
    Middleware-функция для логирования HTTP-запросов FastAPI.

    Сохраняет информацию о запросе: IP клиента, параметры, тело, а также данные пользователя из JWT-токена (если есть).
    Логирует время выполнения, путь, метод, статус ответа, summary и description эндпоинта из OpenAPI.

    Args:
        request (Request): Входящий HTTP-запрос FastAPI.
        call_next (Callable): Следующая функция цепочки обработки запроса.

    Returns:
        Response: HTTP-ответ, возвращённый приложением.
    """
    start_time = time.time()
    # IP-адрес клиента
    client_ip = request.client.host
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    auth_header = request.headers.get("Authorization", "")
    bearer_token = (
        auth_header.replace("Bearer ", "")
        if auth_header.startswith("Bearer ")
        else None
    )

    try:
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8")
        try:
            body = json.loads(body_text)
        except json.JSONDecodeError:
            body = body_text
    except Exception as e:
        body = f"Failed to read body: {e}"

        # Попытка декодировать токен (без верификации)
    user_info = {}
    if bearer_token and app_config.is_keycloak_auth():
        try:
            payload = jwt.get_unverified_claims(bearer_token)
            user_info = {
                "user_id": payload.get("userId") or payload.get("sub"),
                "username": payload.get("preferred_username"),
                "email": payload.get("email"),
                "given_name": payload.get("given_name"),
                "family_name": payload.get("family_name"),
                "realm_roles": payload.get("realm_access", {}).get("roles", []),
            }
        except Exception as e:
            user_info = {"token_decode_error": str(e)}

    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    route = request.scope.get("route")
    route_path = "/"
    if route:
        route_path = route.path
    method = request.method.lower()
    actions_descriptions = get_summary(route_path, method)

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "query": dict(request.query_params),
        "body": body,
        "status_code": response.status_code,
        "duration_sec": process_time,
        "client_ip": client_ip,
        "summary": actions_descriptions["summary"],
        "description": actions_descriptions["description"],
        **user_info,
    }

    logger.info(log_data)
    return response


def get_summary(route_path, method):
    """
    Получает summary и description для маршрута из OpenAPI схемы FastAPI.

    Args:
        route_path (str): Путь маршрута (например, "/api/items").
        method (str): HTTP-метод (например, "get", "post").

    Returns:
        dict: Словарь с ключами "summary" и "description".
    """
    from app.main import app

    actions_descriptions = {
        "summary": "...",
        "description": "...",
    }
    if not app.openapi_schema:
        app.openapi()
    if app.openapi_schema:
        summary = (
            app.openapi_schema.get("paths", {})
            .get(route_path, {})
            .get(method, {})
            .get("summary", "")
        )
        actions_descriptions["summary"] = summary
        description = (
            app.openapi_schema.get("paths", {})
            .get(route_path, {})
            .get(method, {})
            .get("description", "")
        )
        actions_descriptions["description"] = description
    return actions_descriptions
