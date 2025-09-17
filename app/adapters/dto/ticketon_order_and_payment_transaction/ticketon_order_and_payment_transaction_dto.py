from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.shared.dto_constants import DTOConstant


class TicketonOrderAndPaymentTransactionDTO(BaseModel):
    """Базовый DTO для связи заказа Ticketon и платежной транзакции"""
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionCDTO(BaseModel):
    """DTO для создания связи между заказом Ticketon и платежной транзакцией"""

    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи (initial, recreated, refund, etc.)"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionRDTO(BaseModel):
    """DTO для чтения связи между заказом Ticketon и платежной транзакцией"""

    id: DTOConstant.StandardID()
    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )
    created_at: DTOConstant.StandardDateTimeField(
        description="Дата создания"
    )
    updated_at: DTOConstant.StandardDateTimeField(
        description="Дата обновления"
    )
    deleted_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата удаления"
    )

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionWithRelationsRDTO(BaseModel):
    """DTO для чтения связи с полными данными о заказе и транзакции"""

    id: DTOConstant.StandardID()
    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )
    created_at: DTOConstant.StandardDateTimeField(
        description="Дата создания"
    )
    updated_at: DTOConstant.StandardDateTimeField(
        description="Дата обновления"
    )
    deleted_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата удаления"
    )

    # Relationships
    ticketon_order: Optional[TicketonOrderRDTO] = None
    payment_transaction: Optional[PaymentTransactionRDTO] = None

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionFilter(BaseModel):
    """Фильтр для поиска связей"""

    ticketon_order_id: Optional[int] = DTOConstant.StandardNullableIntegerQueryField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: Optional[int] = DTOConstant.StandardNullableIntegerQueryField(
        description="ID платежной транзакции"
    )
    is_active: Optional[bool] = DTOConstant.StandardNullableBooleanQueryField(
        description="Только активные связи"
    )
    is_primary: Optional[bool] = DTOConstant.StandardNullableBooleanQueryField(
        description="Только основные транзакции"
    )
    link_type: Optional[str] = DTOConstant.StandardNullableVarcharQueryField(
        description="Тип связи"
    )
    search: Optional[str] = DTOConstant.StandardSearchQueryField(
        description="Поиск по типу связи или причине"
    )
    order_by: Optional[str] = DTOConstant.StandardOrderByQueryField(
        description="Поле для сортировки"
    )
    order_direction: Optional[str] = DTOConstant.StandardOrderDirectionQueryField(
        description="Направление сортировки"
    )
    is_show_deleted: Optional[bool] = DTOConstant.StandardShowDeletedQueryField(
        description="Показать удаленные записи"
    )

    def apply(self):
        """Применяет фильтры и возвращает список SQLAlchemy фильтров"""
        from app.entities.ticketon_order_and_payment_transaction_entity import TicketonOrderAndPaymentTransactionEntity
        from sqlalchemy import func, or_

        filters = []

        if self.ticketon_order_id is not None:
            filters.append(TicketonOrderAndPaymentTransactionEntity.ticketon_order_id == self.ticketon_order_id)

        if self.payment_transaction_id is not None:
            filters.append(TicketonOrderAndPaymentTransactionEntity.payment_transaction_id == self.payment_transaction_id)

        if self.is_active is not None:
            filters.append(TicketonOrderAndPaymentTransactionEntity.is_active == self.is_active)

        if self.is_primary is not None:
            filters.append(TicketonOrderAndPaymentTransactionEntity.is_primary == self.is_primary)

        if self.link_type:
            filters.append(func.lower(TicketonOrderAndPaymentTransactionEntity.link_type).like(f"%{self.link_type.lower()}%"))

        if self.search:
            search_filter = or_(
                func.lower(TicketonOrderAndPaymentTransactionEntity.link_type).like(f"%{self.search.lower()}%"),
                func.lower(TicketonOrderAndPaymentTransactionEntity.link_reason).like(f"%{self.search.lower()}%")
            )
            filters.append(search_filter)

        return filters

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionPaginationFilter(TicketonOrderAndPaymentTransactionFilter):
    """Фильтр с пагинацией для связей"""

    page: int = DTOConstant.StandardPageQueryField()
    per_page: int = DTOConstant.StandardPerPageQueryField()

    class Config:
        from_attributes = True


# Pagination DTO
from app.shared.dto_pagination_constants import PaginationDTO

class PaginationTicketonOrderAndPaymentTransactionWithRelationsRDTO(
    PaginationDTO[TicketonOrderAndPaymentTransactionWithRelationsRDTO]
):
    """Пагинированный ответ для связей с отношениями"""
    pass


class PaginationTicketonOrderAndPaymentTransactionRDTO(
    PaginationDTO[TicketonOrderAndPaymentTransactionRDTO]
):
    """Пагинированный ответ для связей"""
    pass