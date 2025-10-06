from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_status.product_order_status_dto import ProductOrderStatusRDTO, \
    ProductOrderStatusWithRelationsRDTO
from app.adapters.repository.product_order_status.product_order_status_repository import ProductOrderStatusRepository

from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductOrderStatusByIdCase(BaseUseCase[ProductOrderStatusWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ProductOrderStatusRepository(db)
        self.model: ProductOrderStatusEntity | None = None

    async def execute(self, id: int) -> ProductOrderStatusWithRelationsRDTO:
        await self.validate(id=id)
        return ProductOrderStatusRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id, include_deleted_filter=True,options=self.repository.default_relationships())
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))