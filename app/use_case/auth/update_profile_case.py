from sqlalchemy import or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.register_dto import UpdateProfileDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateProfileCase(BaseUseCase[UserWithRelationsRDTO]):
    """
    Use case для обновления профиля пользователя.

    Атрибуты:
        repository (UserRepository): Репозиторий для работы с пользователями.
        user_id (int): ID пользователя для обновления.
        model: Модель пользователя.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.user_id: int | None = None
        self.model = None

    async def execute(self, user_id: int, dto: UpdateProfileDTO) -> UserWithRelationsRDTO:
        self.user_id = user_id
        await self.validate(dto)
        await self.transform(dto)

        updated_model = await self.repository.update(obj=self.model, dto=dto)
        if updated_model:
            updated_model = await self.repository.get(
                id=updated_model.id,
                options=self.repository.default_relationships(),
                include_deleted_filter=True
            )
            return UserWithRelationsRDTO.from_orm(updated_model)

        raise AppExceptionResponse.internal_error(
            message=i18n.gettext("something_went_wrong")
        )

    async def validate(self, dto: UpdateProfileDTO) -> None:
        # Проверяем, что пользователь существует
        self.model = await self.repository.get(id=self.user_id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Проверяем уникальность email, phone, iin (исключая текущего пользователя)
        existing_user = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    func.lower(self.repository.model.email) == dto.email.lower(),
                    func.lower(self.repository.model.phone) == dto.phone.lower(),
                    func.lower(self.repository.model.iin) == dto.iin.lower() if dto.iin else None,
                ),
                self.repository.model.id != self.user_id
            ]
        )

        if existing_user:
            if existing_user.email.lower() == dto.email.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("email_exists")
                )
            if existing_user.phone.lower() == dto.phone.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("phone_exists")
                )
            if dto.iin and existing_user.iin and existing_user.iin.lower() == dto.iin.lower():
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("iin_exists")
                )

    async def transform(self, dto: UpdateProfileDTO) -> None:
        # Дополнительная обработка данных при необходимости
        pass