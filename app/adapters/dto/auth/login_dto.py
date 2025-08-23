from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class LoginDTO(BaseModel):
    """
    DTO для передачи учетных данных пользователя при входе в систему.

    Атрибуты:
        username (str): Имя пользователя для аутентификации.
        password (str): Пароль пользователя.
    """

    username: DTOConstant.StandardTextField(description="Логин для аутентификации")
    password: DTOConstant.StandardTextField(description="Пароль пользователя")
