from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class TicketonShowsImageDTO(BaseModel):
    """DTO для изображения события"""
    url: DTOConstant.StandardNullableVarcharField("URL изображения")
    alt: DTOConstant.StandardNullableVarcharField("Альтернативный текст")
    main: DTOConstant.StandardBooleanFalseField("Основное изображение")
    cover: DTOConstant.StandardBooleanFalseField("Обложка")


class TicketonShowsPriceDTO(BaseModel):
    """DTO для цены билета"""
    type: DTOConstant.StandardNullableVarcharField("Тип цены")
    name: DTOConstant.StandardNullableVarcharField("Название тарифа")
    sum: DTOConstant.StandardIntegerField("Стоимость в тенге")
    discounts: Union[Dict, List] = Field(description="Скидки")
    show_discount: DTOConstant.StandardIntegerDefaultZeroField("Показать скидку")


class TicketonShowsCityDTO(BaseModel):
    """DTO для города"""
    id: DTOConstant.StandardID("ID города")
    tag: DTOConstant.StandardVarcharField("Тег города")
    name: DTOConstant.StandardVarcharField("Название города")


class TicketonShowsPlaceDTO(BaseModel):
    """DTO для места проведения"""
    id: DTOConstant.StandardID("ID места")
    driver: DTOConstant.StandardNullableVarcharField("Драйвер")
    is_active: DTOConstant.StandardBooleanTrueField("Активность места")
    contact: DTOConstant.StandardNullableVarcharField("Контакт")
    city_id: DTOConstant.StandardID("ID города")
    kinokz_id: DTOConstant.StandardNullableIntegerField("ID в системе Kinokz")
    time_shift: DTOConstant.StandardIntegerDefaultZeroField("Сдвиг времени")
    name: DTOConstant.StandardVarcharField("Название места")
    remark: DTOConstant.StandardNullableTextField("Примечание")
    address: DTOConstant.StandardNullableTextField("Адрес")
    namefull: DTOConstant.StandardNullableVarcharField("Полное название")
    description: DTOConstant.StandardNullableTextField("Описание")
    images: Union[Dict, List] = Field(description="Изображения места")
    main: DTOConstant.StandardNullableVarcharField("Основное изображение")


class TicketonShowsEventDTO(BaseModel):
    """DTO для события"""
    id: DTOConstant.StandardID("ID события")
    duration: DTOConstant.StandardNullableIntegerField("Длительность в минутах")
    kinokz_id: DTOConstant.StandardNullableIntegerField("ID в системе Kinokz")
    fcsk: DTOConstant.StandardNullableVarcharField("FCSK")
    type: DTOConstant.StandardNullableVarcharField("Тип события")
    rating_kp: DTOConstant.StandardNullableFloatField("Рейтинг КиноПоиск")
    rating_imdb: DTOConstant.StandardNullableFloatField("Рейтинг IMDB")
    uri: DTOConstant.StandardNullableVarcharField("URI события")
    premiere_ts: DTOConstant.StandardNullableIntegerField("Timestamp премьеры")
    kzpremiere_ts: DTOConstant.StandardNullableIntegerField("Timestamp премьеры в КЗ")
    url: DTOConstant.StandardNullableVarcharField("URL события")
    director: DTOConstant.StandardNullableVarcharField("Режиссер")
    actors: DTOConstant.StandardNullableTextField("Актеры")
    country: DTOConstant.StandardNullableVarcharField("Страна")
    year: DTOConstant.StandardNullableVarcharField("Год")
    is_main: DTOConstant.StandardBooleanFalseField("Основное событие")
    is_top: DTOConstant.StandardBooleanFalseField("Топ событие")
    solded_count_d: DTOConstant.StandardIntegerDefaultZeroField("Продано билетов (день)")
    recommended_d: DTOConstant.StandardIntegerDefaultZeroField("Рекомендуемое (день)")
    hide_date: DTOConstant.StandardBooleanFalseField("Скрыть дату")
    is_sulpak_cinema: DTOConstant.StandardBooleanFalseField("Сулпак кинотеатр")
    priority: DTOConstant.StandardIntegerDefaultZeroField("Приоритет")
    city_id: DTOConstant.StandardNullableIntegerField("ID города")
    strict_showings: DTOConstant.StandardBooleanFalseField("Строгие показы")
    name: DTOConstant.StandardVarcharField("Название события")
    remark: DTOConstant.StandardNullableTextField("Примечание")
    genre: DTOConstant.StandardNullableVarcharField("Жанр")
    description: DTOConstant.StandardNullableTextField("Описание")
    information: DTOConstant.StandardNullableTextField("Информация")
    access_restrict: DTOConstant.StandardIntegerDefaultZeroField("Ограничение доступа")
    images: List[TicketonShowsImageDTO] = Field(description="Изображения события")
    video: Union[Dict, List] = Field(description="Видео")
    solded_count: DTOConstant.StandardNullableVarcharField("Продано билетов")
    recommended: DTOConstant.StandardIntegerDefaultZeroField("Рекомендуемое")
    information2: Optional[Union[Dict, List]] = Field(default=None, description="Дополнительная информация")
    cover: DTOConstant.StandardNullableVarcharField("Обложка")
    main: DTOConstant.StandardNullableVarcharField("Основное изображение")


class TicketonShowsShowDTO(BaseModel):
    """DTO для сеанса"""
    id: DTOConstant.StandardID("ID сеанса")
    place: DTOConstant.StandardID("ID места")
    hall_id: DTOConstant.StandardID("ID зала")
    event: DTOConstant.StandardID("ID события")
    ts: DTOConstant.StandardNullableVarcharField("Timestamp")
    hall: DTOConstant.StandardNullableVarcharField("Зал")
    lang: DTOConstant.StandardNullableVarcharField("Язык")
    format: DTOConstant.StandardNullableVarcharField("Формат")
    shift: DTOConstant.StandardNullableVarcharField("Сдвиг")
    name: DTOConstant.StandardNullableVarcharField("Название сеанса")
    is_native_widget: DTOConstant.StandardBooleanFalseField("Нативный виджет")
    session_format: DTOConstant.StandardNullableVarcharField("Формат сессии")
    session_id: DTOConstant.StandardNullableVarcharField("ID сессии")
    dt: DTOConstant.StandardNullableDateTimeField("Дата и время сеанса")
    prices: List[TicketonShowsPriceDTO] = Field(description="Цены на билеты")


class TicketonShowsDataDTO(BaseModel):
    """Основной DTO для данных о сеансах"""
    places: Dict[int, TicketonShowsPlaceDTO] = Field(description="Места проведения")
    events: Dict[int, TicketonShowsEventDTO] = Field(description="События")
    shows: Dict[int, TicketonShowsShowDTO] = Field(description="Сеансы")
    cities: Dict[int, TicketonShowsCityDTO] = Field(description="Города")

    @classmethod
    def from_json(cls, data: dict) -> "TicketonShowsDataDTO":
        """Создание DTO из JSON данных"""
        return cls(
            places={
                int(k): TicketonShowsPlaceDTO(**v)
                for k, v in data.get("places", {}).items()
            },
            events={
                int(k): TicketonShowsEventDTO(**v)
                for k, v in data.get("events", {}).items()
            },
            shows={
                int(k): TicketonShowsShowDTO(**v)
                for k, v in data.get("shows", {}).items()
            },
            cities={
                int(k): TicketonShowsCityDTO(**v)
                for k, v in data.get("cities", {}).items()
            }
        )

    def get_valid_shows(self) -> List[TicketonShowsShowDTO]:
        """Возвращает только валидные сеансы с полными связанными данными"""
        valid_shows = []

        for show in self.shows.values():
            place = self.places.get(show.place)
            event = self.events.get(show.event)
            city = self.cities.get(place.city_id) if place else None

            if place and event and city:
                valid_shows.append(show)

        return valid_shows

    def get_show_with_details(self, show_id: int) -> Optional[dict]:
        """Возвращает сеанс с полной информацией"""
        show = self.shows.get(show_id)
        if not show:
            return None

        place = self.places.get(show.place)
        event = self.events.get(show.event)
        city = self.cities.get(place.city_id) if place else None

        if not (place and event and city):
            return None

        return {
            "show": show,
            "event": event,
            "place": place,
            "city": city
        }

    def get_shows_for_city(self, city_id: int) -> List[TicketonShowsShowDTO]:
        """Возвращает все сеансы для определенного города"""
        city_shows = []

        for show in self.get_valid_shows():
            place = self.places.get(show.place)
            if place and place.city_id == city_id:
                city_shows.append(show)

        return city_shows

    def get_shows_for_event(self, event_id: int) -> List[TicketonShowsShowDTO]:
        """Возвращает все сеансы для определенного события"""
        return [show for show in self.get_valid_shows() if show.event == event_id]



class TicketonGetShowsParameterDTO(BaseModel):
    place: Optional[int] = Field(default=None, description="ID площадки (place[])")
    withParam: Optional[str] = Field(default="future", alias="with", description="Состояние (with[])")
    i18n: Optional[str] = Field(default="ru", description="Язык локализации (i18n)")
    type: Optional[str] = Field(default="sport", description="Категория (type[])")


class TicketonShowsRedisStore(BaseModel):
    query: TicketonGetShowsParameterDTO
    data: TicketonShowsDataDTO
    last_updated: datetime