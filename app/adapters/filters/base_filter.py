from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Query as SQLAlchemyQuery

T = TypeVar("T")


class BaseFilter(Generic[T], ABC):
    """
    Базовый класс с фильтрацией.

    Позволяет реализовать фильтрацию для моделей.

    Атрибуты:
        model (T): Модель SQLAlchemy, к которой применяется фильтрация.
        search (str | None): Строка поиска, применяемая к заданным полям.
        order_by (str | None): Поле для сортировки.
        order_direction (str): Направление сортировки ('asc' или 'desc', по умолчанию 'asc').
    """

    def __init__(
        self,
        model: T,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: str | None = "asc",
    ) -> None:
        """
        Инициализация базового с фильтрации.
        """
        self.model = model
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction

    @abstractmethod
    def get_search_filters(self) -> list[str] | None:
        """
        Возвращает список полей, по которым выполняется поиск.
        """

    @abstractmethod
    def apply(self) -> list[SQLAlchemyQuery]:
        """
        Применяет фильтрацию и возвращает список SQLAlchemy-запросов.
        """
