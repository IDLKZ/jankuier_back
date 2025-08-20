from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BasePaginationFilter(Generic[T], ABC):
    """
    Базовый класс для пагинации с фильтрацией.

    Позволяет реализовать фильтрацию и пагинацию для моделей.

    Атрибуты:
        model (T): Модель SQLAlchemy, к которой применяется фильтрация.
        per_page (int): Количество элементов на одной странице (по умолчанию 20).
        page (int): Номер текущей страницы (по умолчанию 1).
        search (str | None): Строка поиска, применяемая к заданным полям.
        order_by (str | None): Поле для сортировки.
        order_direction (str): Направление сортировки ('asc' или 'desc', по умолчанию 'asc').
    """

    def __init__(
        self,
        model: T,
        per_page: int = 20,
        page: int = 1,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: str = "asc",
    ) -> None:
        """
        Инициализация базового фильтрации с пагинацией.
        """
        self.model = model
        self.per_page = per_page
        self.page = page
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction

    @abstractmethod
    def get_search_filters(self) -> list[str] | None:
        """
        Возвращает список полей, по которым выполняется поиск.
        """

    @abstractmethod
    def apply(self) -> list:
        """
        Применяет фильтрацию и возвращает список SQLAlchemy-запросов.
        """
