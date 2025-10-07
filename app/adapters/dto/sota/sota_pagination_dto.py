from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant

T = TypeVar("T")


class SotaPaginationResponseDTO(BaseModel, Generic[T]):
    count: DTOConstant.StandardUnsignedIntegerField("Количество элементов")
    next: DTOConstant.StandardNullableTextField("Ссылка на следующую страницу")
    previous: DTOConstant.StandardNullableTextField("Ссылка на предыдущую страницу")
    results: List[T]