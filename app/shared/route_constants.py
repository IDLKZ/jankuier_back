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

    PaymentTransactionStatusPathName = "/payment-transaction-status"
    PaymentTransactionStatusTagName = "Статус платежной транзакции"

    PaymentTransactionPathName = "/payment-transaction"
    PaymentTransactionTagName = "Платежная транзакция"

    TicketonOrderStatusPathName = "/ticketon-order-status"
    TicketonOrderStatusTagName = "Статус заказа Ticketon"

    TicketonOrderPathName = "/ticketon-order"
    TicketonOrderTagName = "Заказ Ticketon"

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
    UpdateProfilePathName = "/update-profile"
    UpdatePasswordPathName = "/update-password"
    UpdateProfilePhotoPathName = "/update-profile-photo"
    DeleteProfilePhotoPathName = "/delete-profile-photo"
    TestGetPathName = "/test-get"
    TestPostPathName = "/test-post"
    
    # User Cart paths
    UserCartPathName = "/user-cart"
    UserCartTagName = "Корзина пользователя"
