from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.cart.cart_repository import CartRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteCartCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления корзины.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.
        model (CartEntity | None): Удаляемая модель корзины.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartRepository(db)
        self.model: CartEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления корзины.

        Args:
            id (int): Идентификатор корзины для удаления.
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
            id (int): Идентификатор корзины для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("cart_id_validation_error")
            )

        # Проверка существования корзины
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(i18n.gettext("cart_not_found"))

        # Бизнес-правила для удаления
        if not force_delete:
            # Дополнительные бизнес-проверки (если нужны):
            # - Проверка на активные заказы, связанные с корзиной
            # - Проверка на право доступа к корзине
            # - Другие бизнес-ограничения

            # Проверка на пустую корзину (предупреждение о потере данных)
            if model.cart_items and len(model.cart_items) > 0:
                # Можно добавить дополнительную логику или просто разрешить удаление
                pass

        self.model = model

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
