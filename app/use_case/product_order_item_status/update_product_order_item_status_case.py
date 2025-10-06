from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item_status.product_order_item_status_dto import ProductOrderItemStatusRDTO, ProductOrderItemStatusCDTO
from app.adapters.repository.product_order_item_status.product_order_item_status_repository import ProductOrderItemStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderItemStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateProductOrderItemStatusCase(BaseUseCase[ProductOrderItemStatusRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ProductOrderItemStatusRepository(db)
        self.model: ProductOrderItemStatusEntity | None = None

    async def execute(self, id: int, dto: ProductOrderItemStatusCDTO) -> ProductOrderItemStatusRDTO:
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return ProductOrderItemStatusRDTO.from_orm(model)

    async def validate(self, id: int, dto: ProductOrderItemStatusCDTO) -> None:
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Проверяем уникальность title_ru (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.title_ru == dto.title_ru,
                )
            ],
            include_deleted_filter=True,
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