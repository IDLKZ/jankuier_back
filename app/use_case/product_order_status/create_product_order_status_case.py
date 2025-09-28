from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_status.product_order_status_dto import ProductOrderStatusCDTO, ProductOrderStatusRDTO
from app.adapters.repository.product_order_status.product_order_status_repository import ProductOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateProductOrderStatusCase(BaseUseCase[ProductOrderStatusRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ProductOrderStatusRepository(db)
        self.model: ProductOrderStatusEntity | None = None

    async def execute(self, dto: ProductOrderStatusCDTO) -> ProductOrderStatusRDTO:
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return ProductOrderStatusRDTO.from_orm(model)

    async def validate(self, dto: ProductOrderStatusCDTO) -> None:
        # Проверяем уникальность title_ru
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.title_ru == dto.title_ru]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )

        # Валидация previous_id если указан
        if dto.previous_id is not None:
            previous_status = await self.repository.get(dto.previous_id)
            if not previous_status:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("previous_status_not_found")
                )

        # Валидация next_id если указан
        if dto.next_id is not None:
            next_status = await self.repository.get(dto.next_id)
            if not next_status:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("next_status_not_found")
                )

        self.model = ProductOrderStatusEntity(**dto.dict())