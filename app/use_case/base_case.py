from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseUseCase(ABC, Generic[T]):
    """
    Базовый класс для всех Use Cases.
    Все Use Cases должны наследоваться от этого класса и реализовать метод execute. validate. transform.
    execute - основная логика use cases
    validate - валидация входных данных
    transform - преобразование входных данных в выходные данные
    """

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> T:
        pass

    @abstractmethod
    async def validate(self, *args: Any, **kwargs: Any):
        pass

    async def transform(self, *args: Any, **kwargs: Any):
        pass
