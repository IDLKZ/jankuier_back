from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteCartItemCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления товара из корзины.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.
        model (CartItemEntity | None): Удаляемая модель товара в корзине.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)
        self.model: CartItemEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления товара из корзины.

        Args:
            id (int): Идентификатор товара в корзине для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)
        
        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор товара в корзине для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("cart_item_id_validation_error")
            )

        # Проверка существования товара в корзине
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("cart_item_not_found")
            )

        # Бизнес-правила для удаления
        if not force_delete:
            # Дополнительные бизнес-проверки (если нужны):
            # - Проверка на активные заказы, содержащие данный товар
            # - Проверка прав доступа к корзине
            # - Другие бизнес-ограничения
            
            # Например, можно проверить, не заблокирована ли корзина для изменений
            # if model.cart.is_locked:
            #     raise AppExceptionResponse.bad_request("Cart is locked for modifications")
            
            pass

        self.model = model

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass