from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.product_order.product_order_dto import  ProductOrderCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CancelOrDeleteOrderCase(BaseUseCase[bool]):

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозиториев для работы с данными
        self.product_order_repository = ProductOrderRepository(db)
        self.product_order_item_repository = ProductOrderItemRepository(db)

        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь
        self.product_order_id: int | None = None  # ID заказа для пересоздания
        self.is_delete: bool  = False  # ID заказа для пересоздания
        self.future_status_id = DbValueConstants.ProductOrderStatusCancelledID
        self.future_item_status_id = DbValueConstants.ProductOrderItemStatusCancelledID

    async def execute(self, id: int, user: UserWithRelationsRDTO,is_delete:bool = False) -> bool:
        # Подготовка входных данных
        self.current_user = user
        self.product_order_id = id
        self.is_delete = is_delete
        # Выполнение основной логики
        await self.validate()
        return await self.transform()



    async def validate(self) -> None:

        if self.product_order_id is None or self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        self.current_product_order = await self.product_order_repository.get_first_with_filters(
            filters=[
                self.product_order_repository.model.id == self.product_order_id,
                self.product_order_repository.model.user_id == self.current_user.id
            ],
            options=self.product_order_repository.default_relationships()
        )
        if not self.current_product_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        if self.current_product_order.is_active is False or self.current_product_order.is_canceled is True or self.current_product_order.status_id not in [
            DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,
            DbValueConstants.ProductOrderStatusPaidID,#В этом случае будем ожидать возврата средств

        ]:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_is_not_active"))

    async def transform(self) -> bool:
        try:
            if self.current_product_order.status_id == DbValueConstants.ProductOrderStatusPaidID:
                self.future_status_id = DbValueConstants.ProductOrderStatusCancelledAwaitingRefundID
                self.future_item_status_id = DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID
                self.is_delete = False
            else:
                self.future_status_id = DbValueConstants.ProductOrderStatusCancelledID

            if self.is_delete:
                await self.product_order_repository.delete(id=self.product_order_id, force_delete=True)
                return True
            else:
                product_cdto = ProductOrderCDTO.from_orm(self.current_product_order)
                product_cdto.is_active = False
                product_cdto.is_canceled = True
                product_cdto.status_id = self.future_status_id
                product_cdto.canceled_by_id = self.current_user.id
                await self.product_order_repository.update(obj=self.current_product_order, dto=product_cdto)

                product_items = await self.product_order_item_repository.get_with_filters(
                    filters=[
                        self.product_order_item_repository.model.order_id == self.product_order_id]
                )
                if product_items:
                    for item in product_items:
                        await self.product_order_item_repository.update(
                            obj=item,
                            dto={
                                "status_id": self.future_item_status_id,
                            }
                        )
                return True


        except Exception as exc:
            return False








