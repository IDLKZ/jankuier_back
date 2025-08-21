import json
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartUpdateDTO, CartRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateCartCase(BaseUseCase[CartRDTO]):
    """
    Класс Use Case для обновления корзины.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - DTO `CartUpdateDTO` для входных данных.
        - DTO `CartRDTO` для возврата данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.
        model (CartEntity | None): Обновляемая модель корзины.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartRepository(db)
        self.model: CartEntity | None = None

    async def execute(self, id: int, dto: CartUpdateDTO) -> CartRDTO:
        """
        Выполняет операцию обновления корзины.

        Args:
            id (int): Идентификатор корзины.
            dto (CartUpdateDTO): Данные для обновления корзины.

        Returns:
            CartRDTO: Обновленная корзина.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return CartRDTO.from_orm(model)

    async def validate(self, id: int, dto: CartUpdateDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор корзины.
            dto (CartUpdateDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования корзины
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("cart_not_found")
            )

        # Валидация общей стоимости (если обновляется)
        if dto.total_price is not None and dto.total_price < Decimal('0'):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_total_calculation_error")
            )

        # Валидация JSON данных корзины (если обновляются)
        if dto.cart_items is not None:
            self._validate_cart_items_json(dto.cart_items)

    def _validate_cart_items_json(self, cart_items: any) -> None:
        """
        Валидация JSON данных товаров корзины.

        Args:
            cart_items: JSON данные товаров корзины.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        try:
            if isinstance(cart_items, str):
                parsed_items = json.loads(cart_items)
            elif isinstance(cart_items, (dict, list)):
                parsed_items = cart_items
            else:
                raise ValueError("Invalid JSON format")
            
            # Дополнительная валидация структуры товаров (если нужно)
            if isinstance(parsed_items, list):
                for item in parsed_items:
                    if not isinstance(item, dict):
                        raise ValueError("Each cart item must be an object")
                    # Можно добавить проверки обязательных полей товара
                    
        except (json.JSONDecodeError, ValueError):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_items_invalid_format")
            )

    async def transform(self, id: int, dto: CartUpdateDTO) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор корзины.
            dto (CartUpdateDTO): Данные для преобразования.
        """
        self.model = await self.repository.get(id)

        # Дополнительная обработка данных (если нужно)
        # Например, автоматический пересчет total_price на основе cart_items
        if dto.cart_items is not None and dto.total_price is None:
            # Логика автоматического расчета общей стоимости
            # на основе данных товаров в cart_items
            calculated_total = self._calculate_total_from_items(dto.cart_items)
            if calculated_total is not None:
                dto.total_price = calculated_total

    def _calculate_total_from_items(self, cart_items: any) -> Decimal | None:
        """
        Расчет общей стоимости корзины на основе товаров.

        Args:
            cart_items: JSON данные товаров корзины.

        Returns:
            Decimal | None: Рассчитанная общая стоимость или None если невозможно рассчитать.
        """
        try:
            if isinstance(cart_items, str):
                items = json.loads(cart_items)
            else:
                items = cart_items

            if not isinstance(items, list):
                return None

            total = Decimal('0')
            for item in items:
                if isinstance(item, dict):
                    # Предполагается структура с полями quantity, price или total_price
                    item_total = item.get('total_price') or (
                        item.get('quantity', 0) * item.get('price', 0)
                    )
                    if item_total:
                        total += Decimal(str(item_total))

            return total

        except (json.JSONDecodeError, ValueError, TypeError):
            return None