from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartRDTO, PaginationCartRDTO
from app.adapters.filter.pagination_filter import PaginationFilter
from app.adapters.repository.cart.cart_repository import CartRepository
from app.use_case.base_case import BaseUseCase


class PaginateCartsCase(BaseUseCase[PaginationCartRDTO]):
    """
    Класс Use Case для получения корзин с пагинацией.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - Фильтр `PaginationFilter` для применения условий поиска, сортировки и пагинации.
        - DTO `PaginationCartRDTO` для возврата данных с пагинацией.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.

    Методы:
        execute(filter: PaginationFilter) -> PaginationCartRDTO:
            Выполняет запрос и возвращает корзины с пагинацией.
        validate(filter: PaginationFilter):
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

    async def execute(self, filter: PaginationFilter) -> PaginationCartRDTO:
        """
        Выполняет операцию получения корзин с пагинацией.

        Args:
            filter (PaginationFilter): Объект фильтра с параметрами поиска, сортировки и пагинации.

        Returns:
            PaginationCartRDTO: Пагинированный список корзин.
        """
        await self.validate(filter)
        
        # Применяем фильтры
        filters = []
        if hasattr(filter, 'search') and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по ID пользователя, общей стоимости или данным пользователя
            filters.append(
                or_(
                    func.cast(self.repository.model.user_id, func.text('TEXT')).like(search_term),
                    func.cast(self.repository.model.total_price, func.text('TEXT')).like(search_term),
                    func.lower(self.repository.model.user.username).like(search_term),
                    func.lower(self.repository.model.user.email).like(search_term),
                )
            )
        
        # Получаем данные из репозитория с пагинацией
        result = await self.repository.paginate(
            dto=CartRDTO,
            filters=filters,
            page=filter.page,
            per_page=filter.per_page,
            order_by=getattr(filter, 'order_by', 'created_at'),
            order_direction=getattr(filter, 'order_direction', 'desc'),
            include_deleted_filter=not getattr(filter, 'is_show_deleted', False),
            options=self.repository.default_relationships(),
        )
        
        return result

    async def validate(self, filter: PaginationFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (PaginationFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass