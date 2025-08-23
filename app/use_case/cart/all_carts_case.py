from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartRDTO
from app.adapters.filters.base_filter import BaseFilter
from app.adapters.repository.cart.cart_repository import CartRepository
from app.use_case.base_case import BaseUseCase


class AllCartsCase(BaseUseCase[list[CartRDTO]]):
    """
    Класс Use Case для получения всех корзин с фильтрацией.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `CartRDTO` для возврата данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.

    Методы:
        execute(filter: BaseFilter) -> list[CartRDTO]:
            Выполняет запрос и возвращает список корзин.
        validate(filter: BaseFilter):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartRepository(db)

    async def execute(self, filter: BaseFilter) -> list[CartRDTO]:
        """
        Выполняет операцию получения всех корзин с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[CartRDTO]: Список корзин.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по ID пользователя или общей стоимости
            filters.append(
                or_(
                    func.cast(self.repository.model.user_id, func.text("TEXT")).like(
                        search_term
                    ),
                    func.cast(
                        self.repository.model.total_price, func.text("TEXT")
                    ).like(search_term),
                    func.lower(self.repository.model.user.username).like(search_term),
                    func.lower(self.repository.model.user.email).like(search_term),
                )
            )

        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, "order_by", "created_at"),
            order_direction=getattr(filter, "order_direction", "desc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return [CartRDTO.from_orm(model) for model in models]

    async def validate(self, filter: BaseFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (BaseFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
