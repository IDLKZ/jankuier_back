from pathlib import Path
from typing import Annotated

from app.shared.field_constants import FieldConstants


class RoutePathConstants:
    """
    Системные контанты для роутизации и отображении в SWAGGER
    """

    AuthPathName = "/auth"
    AuthTagName = "Аутентификация"

    FilePathName = "/file"
    FileTagName = "Файл"

    RolePathName = "/role"
    RoleTagName = "Роль"

    PermissionPathName = "/permission"
    PermissionTagName = "Разрешение"

    RolePermissionPathName = "/role-permission"
    RolePermissionTagName = "Права ролей"

    UserPathName = "/user"
    UserTagName = "Пользователь"

    IDPath = Annotated[int, Path(gt=0, description="Уникальный идентификатор")]
    ValuePath = Annotated[
        str,
        Path(
            max_length=FieldConstants.STANDARD_LENGTH, description="Уникальное значение"
        ),
    ]
    BasePathName = "/api"
    EmployeePathName = "/employee"
    ClientPathName = "/client"

    IndexPathName = "/"
    AllPathName = "/all"
    CreatePathName = "/create"
    UpdatePathName = "/update/{id}"
    GetByIdPathName = "/get/{id}"
    GetFullProductByIdPathName = "/get-full-product/{id}"
    DeleteByIdPathName = "/delete/{id}"
    RecoverByIdPathName = "/recover/{id}"
    GetByValuePathName = "/get-by-value/{value}"
    LoginPathName = "/login"
    RegisterPathName = "/register"
    LoginSwaggerPathName = "/login-swagger"
    ResetPasswordPathName = "/reset-password"
    GetMePathName = "/me"
    TestGetPathName = "/test-get"
    TestPostPathName = "/test-post"
