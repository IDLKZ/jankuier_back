from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class TicketonShowLevelSeatDTO(BaseModel):
    """DTO для места в зале"""
    level: DTOConstant.StandardNullableIntegerField("Уровень места")
    w: DTOConstant.StandardNullableVarcharField("Ширина места")
    h: DTOConstant.StandardNullableVarcharField("Высота места")
    rot: DTOConstant.StandardNullableIntegerField("Поворот места")
    id: DTOConstant.StandardNullableVarcharField("ID места")
    row: DTOConstant.StandardNullableVarcharField("Номер ряда")
    num: DTOConstant.StandardNullableIntegerField("Номер места")
    x: DTOConstant.StandardNullableVarcharField("X координата")
    y: DTOConstant.StandardNullableVarcharField("Y координата")
    type: DTOConstant.StandardNullableVarcharField("Тип места")
    sale: DTOConstant.StandardNullableIntegerField("Статус продажи")
    status: DTOConstant.StandardNullableIntegerField("Статус места")
    count: DTOConstant.StandardNullableIntegerField("Количество")
    busy: DTOConstant.StandardNullableIntegerField("Занятость места")


class TicketonShowLevelObjectDTO(BaseModel):
    """DTO для объектов на схеме зала"""
    id: DTOConstant.StandardNullableVarcharField("ID объекта")
    level: DTOConstant.StandardNullableIntegerField("Уровень объекта")
    w: DTOConstant.StandardNullableIntegerField("Ширина объекта")
    h: DTOConstant.StandardNullableIntegerField("Высота объекта")
    x: DTOConstant.StandardNullableIntegerField("X координата объекта")
    y: DTOConstant.StandardNullableIntegerField("Y координата объекта")
    map: DTOConstant.StandardNullableStringField("Карта")
    color: DTOConstant.StandardNullableVarcharField("Цвет объекта")
    name: DTOConstant.StandardNullableVarcharField("Название объекта")
    svg: DTOConstant.StandardNullableStringField("SVG данные")
    svg_text: DTOConstant.StandardNullableStringField("SVG текст")
    svg_text_attrs: DTOConstant.StandardNullableStringField("SVG атрибуты текста")
    type: DTOConstant.StandardNullableVarcharField("Тип объекта")


class TicketonShowLevelTypeDTO(BaseModel):
    """DTO для типа билета"""
    type: DTOConstant.StandardNullableVarcharField("Тип билета")
    sum: DTOConstant.StandardNullableIntegerField("Стоимость билета")
    name: DTOConstant.StandardNullableVarcharField("Название типа")
    type_name: DTOConstant.StandardNullableVarcharField("Название типа билета")
    com: DTOConstant.StandardNullableIntegerField("Комиссия")
    promo: DTOConstant.StandardNullableIntegerField("Промо")
    discounts: Optional[List] = Field(description="Скидки", default=None)


class TicketonShowLevelDataDTO(BaseModel):
    """DTO для данных уровня зала"""
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
    seats: Optional[List[TicketonShowLevelSeatDTO]] = Field(description="Места на уровне", default=None)
    objects: Optional[List[TicketonShowLevelObjectDTO]] = Field(description="Объекты на уровне", default=None)
    types: Optional[Dict[str, TicketonShowLevelTypeDTO]] = Field(description="Типы билетов", default=None)
    seats_count: DTOConstant.StandardNullableIntegerField("Общее количество мест")
    seats_free: DTOConstant.StandardNullableIntegerField("Количество свободных мест")
    display_num: DTOConstant.StandardNullableIntegerField("Номер для отображения")


class TicketonShowLevelDTO(BaseModel):
    """Основной DTO для уровня зала Ticketon"""
    level: Optional[TicketonShowLevelDataDTO] = Field(description="Данные уровня зала", default=None)

    @classmethod
    def from_json(cls, data: dict) -> "TicketonShowLevelDTO":
        """Создание DTO из JSON данных"""
        # Обработка типов билетов
        types_data = data.get("level", {}).get("types", {})
        processed_types = {}
        
        for type_key, type_value in types_data.items():
            processed_types[type_key] = TicketonShowLevelTypeDTO(**type_value)
        
        # Создание данных уровня
        level_data = data.get("level", {}).copy()
        level_data["types"] = processed_types
        
        # Обработка мест
        seats_data = level_data.get("seats", [])
        level_data["seats"] = [TicketonShowLevelSeatDTO(**seat) for seat in seats_data]
        
        # Обработка объектов
        objects_data = level_data.get("objects", [])
        level_data["objects"] = [TicketonShowLevelObjectDTO(**obj) for obj in objects_data]
        
        return cls(level=TicketonShowLevelDataDTO(**level_data))
    
    def get_available_seats(self) -> List[TicketonShowLevelSeatDTO]:
        """Возвращает список доступных мест"""
        if not self.level or not self.level.seats:
            return []
        return [seat for seat in self.level.seats if seat.sale == 1 and seat.busy == 0]
    
    def get_seats_by_row(self, row: str) -> List[TicketonShowLevelSeatDTO]:
        """Возвращает места по номеру ряда"""
        if not self.level or not self.level.seats:
            return []
        return [seat for seat in self.level.seats if seat.row == row]
    
    def get_seat_by_id(self, seat_id: str) -> TicketonShowLevelSeatDTO | None:
        """Возвращает место по ID"""
        if not self.level or not self.level.seats:
            return None
        for seat in self.level.seats:
            if seat.id == seat_id:
                return seat
        return None
    
    def get_seat_types(self) -> Dict[str, TicketonShowLevelTypeDTO]:
        """Возвращает типы билетов"""
        if not self.level or not self.level.types:
            return {}
        return self.level.types
    
    def get_total_seats(self) -> int:
        """Возвращает общее количество мест"""
        if not self.level or self.level.seats_count is None:
            return 0
        return self.level.seats_count
    
    def get_free_seats_count(self) -> int:
        """Возвращает количество свободных мест"""
        if not self.level or self.level.seats_free is None:
            return 0
        return self.level.seats_free
    
    def get_occupied_seats_count(self) -> int:
        """Возвращает количество занятых мест"""
        total = self.get_total_seats()
        free = self.get_free_seats_count()
        return total - free