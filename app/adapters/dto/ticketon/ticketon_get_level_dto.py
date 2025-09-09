from typing import List, Optional
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class TicketonGetLevelPlaceDTO(BaseModel):
    """DTO для места проведения"""
    id: DTOConstant.StandardNullableVarcharField("ID места проведения")
    city_id: DTOConstant.StandardNullableVarcharField("ID города")
    kinokz_id: DTOConstant.StandardNullableVarcharField("ID в системе Kinokz")
    name: DTOConstant.StandardNullableVarcharField("Название места")
    remark: DTOConstant.StandardNullableTextField("Примечание")
    address: DTOConstant.StandardNullableTextField("Адрес")
    namefull: DTOConstant.StandardNullableVarcharField("Полное название")
    description: DTOConstant.StandardNullableTextField("Описание")


class TicketonGetLevelHallDTO(BaseModel):
    """DTO для зала"""
    id: DTOConstant.StandardNullableVarcharField("ID зала")
    place: DTOConstant.StandardNullableVarcharField("ID места проведения")
    name: DTOConstant.StandardNullableVarcharField("Название зала")


class TicketonGetLevelLevelDTO(BaseModel):
    """DTO для уровня зала"""
    id: DTOConstant.StandardNullableVarcharField("ID уровня")
    name: DTOConstant.StandardNullableVarcharField("Название уровня")
    width: DTOConstant.StandardNullableIntegerField("Ширина уровня")
    height: DTOConstant.StandardNullableIntegerField("Высота уровня")
    unbound_seats: DTOConstant.StandardNullableIntegerField("Несвязанные места")
    lazy_loading: DTOConstant.StandardNullableIntegerField("Ленивая загрузка")
    size_ratio: DTOConstant.StandardNullableIntegerField("Соотношение размеров")
    map: DTOConstant.StandardNullableStringField("Карта уровня")
    svg: DTOConstant.StandardNullableStringField("SVG данные уровня")
    svg_text: DTOConstant.StandardNullableStringField("SVG текст уровня")
    svg_text_attrs: DTOConstant.StandardNullableStringField("SVG атрибуты текста уровня")
    color: DTOConstant.StandardNullableVarcharField("Цвет уровня")
    hall: DTOConstant.StandardNullableVarcharField("Идентификатор зала")


class TicketonGetLevelSeatDTO(BaseModel):
    """DTO для места"""
    level: DTOConstant.StandardNullableIntegerField("Уровень места")
    w: DTOConstant.StandardNullableVarcharField("Ширина места")
    h: DTOConstant.StandardNullableVarcharField("Высота места")
    rot: DTOConstant.StandardNullableIntegerField("Поворот места")
    id: DTOConstant.StandardNullableVarcharField("ID места")
    row: DTOConstant.StandardNullableVarcharField("Номер ряда")
    num: DTOConstant.StandardNullableIntegerField("Номер места")
    x: DTOConstant.StandardNullableVarcharField("X координата")
    y: DTOConstant.StandardNullableVarcharField("Y координата")
    busy: DTOConstant.StandardNullableIntegerField("Занятость места")


class TicketonGetLevelDTO(BaseModel):
    """Основной DTO для получения данных уровня зала Ticketon"""
    status: DTOConstant.StandardNullableIntegerField("Статус ответа")
    place: Optional[TicketonGetLevelPlaceDTO] = Field(description="Данные места проведения", default=None)
    hall: Optional[TicketonGetLevelHallDTO] = Field(description="Данные зала", default=None)
    level: Optional[TicketonGetLevelLevelDTO] = Field(description="Данные уровня", default=None)
    seats: Optional[List[TicketonGetLevelSeatDTO]] = Field(description="Список мест", default=None)

    @classmethod
    def from_json(cls, data: dict) -> "TicketonGetLevelDTO":
        """Создание DTO из JSON данных"""
        # Обработка места проведения
        place_data = data.get("place")
        place_dto = TicketonGetLevelPlaceDTO(**place_data) if place_data else None
        
        # Обработка зала
        hall_data = data.get("hall")
        hall_dto = TicketonGetLevelHallDTO(**hall_data) if hall_data else None
        
        # Обработка уровня
        level_data = data.get("level")
        level_dto = TicketonGetLevelLevelDTO(**level_data) if level_data else None
        
        # Обработка мест
        seats_data = data.get("seats", [])
        seats_dto = [TicketonGetLevelSeatDTO(**seat) for seat in seats_data] if seats_data else None
        
        return cls(
            status=data.get("status"),
            place=place_dto,
            hall=hall_dto,
            level=level_dto,
            seats=seats_dto
        )
    
    def is_success(self) -> bool:
        """Проверяет успешность запроса"""
        return self.status == 1
    
    def get_available_seats(self) -> List[TicketonGetLevelSeatDTO]:
        """Возвращает список доступных мест"""
        if not self.seats:
            return []
        return [seat for seat in self.seats if seat.busy == 0]
    
    def get_seats_by_row(self, row: str) -> List[TicketonGetLevelSeatDTO]:
        """Возвращает места по номеру ряда"""
        if not self.seats:
            return []
        return [seat for seat in self.seats if seat.row == row]
    
    def get_seat_by_id(self, seat_id: str) -> TicketonGetLevelSeatDTO | None:
        """Возвращает место по ID"""
        if not self.seats:
            return None
        for seat in self.seats:
            if seat.id == seat_id:
                return seat
        return None
    
    def get_occupied_seats(self) -> List[TicketonGetLevelSeatDTO]:
        """Возвращает список занятых мест"""
        if not self.seats:
            return []
        return [seat for seat in self.seats if seat.busy == 1]
    
    def get_seats_count(self) -> int:
        """Возвращает общее количество мест"""
        return len(self.seats) if self.seats else 0
    
    def get_available_seats_count(self) -> int:
        """Возвращает количество свободных мест"""
        return len(self.get_available_seats())
    
    def get_occupied_seats_count(self) -> int:
        """Возвращает количество занятых мест"""
        return len(self.get_occupied_seats())
    
    def get_place_name(self) -> str | None:
        """Возвращает название места проведения"""
        return self.place.name if self.place else None
    
    def get_hall_name(self) -> str | None:
        """Возвращает название зала"""
        return self.hall.name if self.hall else None
    
    def get_level_name(self) -> str | None:
        """Возвращает название уровня"""
        return self.level.name if self.level else None
    
    def get_level_dimensions(self) -> tuple[int | None, int | None]:
        """Возвращает размеры уровня (ширина, высота)"""
        if not self.level:
            return None, None
        return self.level.width, self.level.height