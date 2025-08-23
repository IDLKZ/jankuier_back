from sqlalchemy import or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.register_dto import RegisterDTO
from app.adapters.dto.user.user_dto import UserCDTO, UserWithRelationsDTO
from app.adapters.repositories.role.role_repository import RoleRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_password_hash
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class RegisterCase(BaseUseCase[UserWithRelationsDTO]):
    """
    Use case для аутентификации пользователей.

    Атрибуты:
        repository (UserRepository): Репозиторий для работы с пользователями.
    """

    def __init__(self, db: AsyncSession) -> UserWithRelationsDTO:

        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    async def execute(self, dto: RegisterDTO) -> UserWithRelationsDTO:
        await self.validate(dto)
        obj = dto.dict()
        obj["password"] = get_password_hash(obj["password"])
        obj["is_active"] = True
        obj["verified"] = False
        model = await self.repository.create(obj=self.repository.model(**obj))
        if model:
            model = await self.repository.get(
                id=model.id, options=self.repository.default_relationships()
            )
            return UserWithRelationsDTO.from_orm(model)
        raise AppExceptionResponse.internal_error(
            message=i18n.gettext("something_went_wrong")
        )

    async def validate(self, dto: RegisterDTO) -> None:
        role = await self.role_repository.get(dto.role_id)
        if not role:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("role_not_found")
            )
        if role.can_register is False:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("role_cant_register")
            )
        user = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    func.lower(self.repository.model.username) == dto.username.lower(),
                    func.lower(self.repository.model.email) == dto.email.lower(),
                    func.lower(self.repository.model.phone) == dto.phone.lower(),
                    func.lower(self.repository.model.iin) == dto.iin.lower(),
                )
            ]
        )
        if user:
            if user.email.lower() == dto.email.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("email_exists")
                )
            if user.username.lower() == dto.username.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("username_exists")
                )
            if user.phone.lower() == dto.phone.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("phone_exists")
                )
            if user.iin.lower() == dto.iin.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("iin_exists")
                )
