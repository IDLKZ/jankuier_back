from pathlib import Path
from typing import Annotated

from app.shared.field_constants import FieldConstants


class AppPathConstants:
    """
    Системные контанты для роутизации и отображении в SWAGGER
    """

    IDPath = Annotated[int, Path(gt=0, description="Уникальный идентификатор")]
    ValuePath = Annotated[
        str,
        Path(
            max_length=FieldConstants.STANDARD_LENGTH, description="Уникальное значение"
        ),
    ]

    FilePathName = "file"
    FileTagName = "Файлы"


    RolePathName = "role"
    RoleTagName = "Роли"

    PermissionPathName = "permission"
    PermissionTagName = "Права доступа"

    RolePermissionPathName = "role-permission"
    RolePermissionTagName = "Роли и права"

    UserPathName = "user"
    UserTagName = "Пользователи"

    # common_types
    IndexPathName = "/"
    AllPathName = "/all"
    CreatePathName = "/create"
    UpdatePathName = "/update/{id}"
    GetByIdPathName = "/get/{id}"
    DeleteByIdPathName = "/delete/{id}"
    GetByValuePathName = "/get-by-value/{value}"
