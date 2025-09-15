from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from app.shared.dto_constants import DTOConstant


# предполагаю, что DTOConstant уже импортирован из твоего модуля
# from app.shared.dto_constants import DTOConstant


# -------------------------
# БАЗОВЫЕ ВСПОМОГАТЕЛЬНЫЕ DTO
# -------------------------

class TicketonSeatDTO(BaseModel):
    model_config = {"extra": "allow"}

    # В ответе встречаются строки-числа — Pydantic их приведёт.
    id: DTOConstant.StandardNullableUnsignedIntegerField("ID места")
    level: DTOConstant.StandardNullableUnsignedIntegerField("ID уровня/сектора")
    row: Optional[Union[str, int]] = Field(default=None, description="Номер ряда")
    num: Optional[Union[str, int]] = Field(default=None, description="Номер места")
    x: Optional[Union[str, int]] = Field(default=None, description="Координата X")
    y: Optional[Union[str, int]] = Field(default=None, description="Координата Y")
    w: Optional[Union[str, int]] = Field(default=None, description="Ширина")
    h: Optional[Union[str, int]] = Field(default=None, description="Высота")
    rot: DTOConstant.StandardNullableIntegerField("Поворот")
    type: DTOConstant.StandardNullableVarcharField("Тип")
    sale: DTOConstant.StandardNullableIntegerField("Флаг продажи")
    status: DTOConstant.StandardNullableIntegerField("Статус")
    count: DTOConstant.StandardNullableIntegerField("Количество")
    busy: DTOConstant.StandardNullableIntegerField("Занятость")


class TicketonObjectDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID объекта")
    level: DTOConstant.StandardNullableUnsignedIntegerField("ID уровня/сектора")
    name: DTOConstant.StandardNullableVarcharField("Имя объекта")
    type: Optional[Union[str, bool]] = Field(default=None, description="Тип объекта")
    x: DTOConstant.StandardNullableIntegerField("Координата X")
    y: DTOConstant.StandardNullableIntegerField("Координата Y")
    w: DTOConstant.StandardNullableIntegerField("Ширина")
    h: DTOConstant.StandardNullableIntegerField("Высота")
    color: DTOConstant.StandardNullableVarcharField("Цвет")
    map: Optional[Union[Dict, str]] = Field(default=None, description="Данные карты/области")
    svg: DTOConstant.StandardNullableTextField("SVG")
    svg_text: DTOConstant.StandardNullableTextField("Надпись SVG")
    svg_text_attrs: DTOConstant.StandardNullableTextField("Атрибуты надписи SVG")


class TicketonHallLevelDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID уровня")
    name: DTOConstant.StandardNullableVarcharField("Название уровня")
    width: DTOConstant.StandardNullableIntegerField("Ширина сцены/карты уровня")
    height: DTOConstant.StandardNullableIntegerField("Высота сцены/карты уровня")
    unbound_seats: DTOConstant.StandardNullableIntegerField("Свободные места (без привязки)")
    lazy_loading: DTOConstant.StandardNullableIntegerField("Lazy loading")
    size_ratio: DTOConstant.StandardNullableIntegerField("Коэффициент размера")
    map: Optional[Union[Dict, str]] = Field(default=None, description="Карта уровня")
    svg: DTOConstant.StandardNullableTextField("SVG карты уровня")
    svg_text: DTOConstant.StandardNullableTextField("Текст на SVG")
    svg_text_attrs: DTOConstant.StandardNullableTextField("Атрибуты текста SVG")
    color: DTOConstant.StandardNullableVarcharField("Цвет")
    seats: Optional[List[TicketonSeatDTO]] = Field(default=None, description="Список мест")
    objects: Optional[List[TicketonObjectDTO]] = Field(default=None, description="Список объектов")
    types: Optional[Union[List[Dict[str, Any]], List[str], str, Dict[str, Any]]] = Field(default=None, description="Произвольные типы/легенда")
    seats_count: DTOConstant.StandardNullableIntegerField("Количество мест")
    seats_free: DTOConstant.StandardNullableIntegerField("Свободно мест")
    display_num: DTOConstant.StandardNullableIntegerField("Номер отображения")


class TicketonHallDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID зала")
    place: DTOConstant.StandardNullableUnsignedIntegerField("ID площадки")
    name: DTOConstant.StandardNullableVarcharField("Название зала")

    # В ответе levels — это объект-словарь, где ключи — строки ID уровня
    levels: Optional[Dict[str, TicketonHallLevelDTO]] = Field(
        default=None, description="Сектора/уровни зала"
    )


class TicketonCityDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID города")
    name: DTOConstant.StandardNullableVarcharField("Название города")


class TicketonPlaceDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID площадки")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField("ID города")
    kinokz_id: DTOConstant.StandardNullableUnsignedIntegerField("ID KinoKZ")
    name: DTOConstant.StandardNullableVarcharField("Короткое имя площадки")
    namefull: DTOConstant.StandardNullableVarcharField("Полное название площадки")
    address: DTOConstant.StandardNullableVarcharField("Адрес")
    remark: DTOConstant.StandardNullableTextField("Примечание/ремарка (HTML)")
    description: DTOConstant.StandardNullableTextField("Описание")
    driver: DTOConstant.StandardNullableVarcharField("Драйвер/тип интеграции")


class TicketonEventDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID события")
    duration: DTOConstant.StandardNullableUnsignedIntegerField("Длительность, мин")
    kinokz_id: DTOConstant.StandardNullableUnsignedIntegerField("ID KinoKZ")
    fcsk: DTOConstant.StandardNullableVarcharField("FCSK")
    type: DTOConstant.StandardNullableVarcharField("Тип (event type)")
    name: DTOConstant.StandardNullableVarcharField("Название")
    genre: DTOConstant.StandardNullableVarcharField("Жанр")
    nameRu: DTOConstant.StandardNullableVarcharField("Название (RU)")
    remark: DTOConstant.StandardNullableTextField("Описание/ремарка (HTML)")


class TicketonShowDataDTO(BaseModel):
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableUnsignedIntegerField("ID сеанса")
    place: DTOConstant.StandardNullableUnsignedIntegerField("ID площадки")
    hall: DTOConstant.StandardNullableUnsignedIntegerField("ID зала")
    showcase: DTOConstant.StandardNullableUnsignedIntegerField("ID витрины/площадки продаж")
    event: DTOConstant.StandardNullableUnsignedIntegerField("ID события")
    sale: DTOConstant.StandardNullableVarcharField("Флаг продажи")
    ts: DTOConstant.StandardNullableUnsignedIntegerField("UNIX-время начала")
    dt: DTOConstant.StandardNullableVarcharField("ISO-время начала")
    is_canceled: DTOConstant.StandardNullableVarcharField("Отменён")
    canceled_ts: DTOConstant.StandardNullableUnsignedIntegerField("UNIX-время отмены")
    sale_from_ts: DTOConstant.StandardNullableUnsignedIntegerField("UNIX-время открытия продаж")
    max_selection: DTOConstant.StandardNullableUnsignedIntegerField("Макс. мест в заказе")
    tickets_to_one_hands: DTOConstant.StandardNullableUnsignedIntegerField("Ограничение на руки")
    name: DTOConstant.StandardNullableVarcharField("Имя сеанса")
    is_native_widget: DTOConstant.StandardNullableVarcharField("Нативный виджет")
    session_format: DTOConstant.StandardNullableVarcharField("Формат сеанса")
    session_id: DTOConstant.StandardNullableVarcharField("Session ID")
    label: DTOConstant.StandardNullableVarcharField("Метка отображения")
    lang: DTOConstant.StandardNullableVarcharField("Язык")
    format: DTOConstant.StandardNullableVarcharField("Формат")

class TicketonPriceDTO(BaseModel):
    model_config = {"extra": "allow"}

    type: DTOConstant.StandardNullableVarcharField("Тип цены")
    sum: DTOConstant.StandardNullableUnsignedIntegerField("Сумма")
    name: DTOConstant.StandardNullableVarcharField("Название цены")
    type_name: DTOConstant.StandardNullableVarcharField("Название типа цены")
    com: DTOConstant.StandardNullableUnsignedIntegerField("Комиссия")
    promo: DTOConstant.StandardNullableUnsignedIntegerField("Промо")
    discounts: Optional[Union[List[Dict[str, Any]], List[str], str]] = Field(default=None, description="Скидки")

class TicketonSingleShowResponseDTO(BaseModel):
    """
    Корневой DTO для ответа Ticketon /show?...
    """
    model_config = {"extra": "allow"}

    show: Optional[TicketonShowDataDTO] = Field(default=None, description="Данные сеанса")
    seatValidationRules: Optional[Union[List[Dict[str, Any]], List[str], str]] = Field(
        default=None, description="Правила валидации мест/заказа"
    )
    event: Optional[TicketonEventDTO] = Field(default=None)
    place: Optional[TicketonPlaceDTO] = Field(default=None)
    city: Optional[TicketonCityDTO] = Field(default=None)
    hall: Optional[TicketonHallDTO] = Field(default=None)
    prices: Optional[Dict[str, TicketonPriceDTO]] = Field(
        default=None, description="Цены по категориям"
    )

    @classmethod
    def from_json(cls, data: dict) -> "TicketonSingleShowResponseDTO":
        """Создание DTO из JSON данных"""
        # Handle nested hall levels structure
        processed_data = data.copy()
        
        if "hall" in processed_data and processed_data["hall"]:
            hall_data = processed_data["hall"].copy()
            if "levels" in hall_data and hall_data["levels"]:
                # Convert levels dict to proper DTO structure
                levels_dict = {}
                for level_id, level_data in hall_data["levels"].items():
                    levels_dict[str(level_id)] = TicketonHallLevelDTO(**level_data)
                hall_data["levels"] = levels_dict
            processed_data["hall"] = TicketonHallDTO(**hall_data)
        
        # Handle prices structure
        if "prices" in processed_data and processed_data["prices"]:
            prices_dict = {}
            for price_key, price_data in processed_data["prices"].items():
                prices_dict[str(price_key)] = TicketonPriceDTO(**price_data)
            processed_data["prices"] = prices_dict
        
        return cls(**processed_data)
