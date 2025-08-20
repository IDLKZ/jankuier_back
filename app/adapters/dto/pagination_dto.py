from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(Generic[T]):
    """
    Обобщенная модель пагинации.

    Атрибуты:
        current_page (int): Текущая страница.
        last_page (int): Последняя страница.
        total_pages (int): Общее количество страниц.
        total_items (int): Общее количество элементов.
        items (list[T]): Список элементов текущей страницы.
    """

    current_page: int
    per_page: int
    last_page: int
    total_pages: int
    total_items: int
    items: list[T]

    def __init__(
        self,
        items: list[T],
        total_pages: int,
        total_items: int,
        per_page: int,
        page: int,
    ) -> None:
        self.items = items
        self.total_pages = total_pages
        self.total_items = total_items
        self.current_page = page
        self.per_page = per_page
        self.last_page = (total_pages + per_page - 1) // per_page


class BasePageModel(BaseModel):
    """
    Базовая модель пагинации.
    Атрибуты:
       current_page (int): Текущая страница.
       last_page (int): Последняя страница.
       total_pages (int): Общее количество страниц.
       total_items (int): Общее количество элементов.
       items (list[T]): Список элементов текущей страницы.
    """

    current_page: int
    per_page: int
    last_page: int
    total_pages: int
    total_items: int


