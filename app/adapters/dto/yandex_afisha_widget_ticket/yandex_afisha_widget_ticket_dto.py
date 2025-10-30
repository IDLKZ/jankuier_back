from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class YandexAfishaWidgetTicketDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class YandexAfishaWidgetTicketCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения билета"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название мероприятия на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название мероприятия на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название мероприятия на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на английском"
    )
    address_ru: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на русском"
    )
    address_kk: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на казахском"
    )
    address_en: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на английском"
    )
    stadium_ru: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на русском"
    )
    stadium_kk: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на казахском"
    )
    stadium_en: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на английском"
    )
    start_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата и время начала мероприятия"
    )
    yandex_session_id: DTOConstant.StandardTextField(
        description="ID сессии в Яндекс.Афиша"
    )
    yandex_widget_url: DTOConstant.StandardNullableTextField(
        description="URL виджета Яндекс.Афиша"
    )
    is_active: DTOConstant.StandardBooleanFalseField(
        description="Флаг активности билета"
    )

    class Config:
        from_attributes = True


class YandexAfishaWidgetTicketRDTO(YandexAfishaWidgetTicketDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения билета"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название мероприятия на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название мероприятия на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название мероприятия на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание мероприятия на английском"
    )
    address_ru: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на русском"
    )
    address_kk: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на казахском"
    )
    address_en: DTOConstant.StandardNullableVarcharField(
        description="Адрес мероприятия на английском"
    )
    stadium_ru: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на русском"
    )
    stadium_kk: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на казахском"
    )
    stadium_en: DTOConstant.StandardNullableVarcharField(
        description="Название стадиона на английском"
    )
    start_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата и время начала мероприятия"
    )
    yandex_session_id: DTOConstant.StandardTextField(
        description="ID сессии в Яндекс.Афиша"
    )
    yandex_widget_url: DTOConstant.StandardNullableTextField(
        description="URL виджета Яндекс.Афиша"
    )
    is_active: DTOConstant.StandardBooleanFalseField(
        description="Флаг активности билета"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class YandexAfishaWidgetTicketWithRelationsRDTO(YandexAfishaWidgetTicketRDTO):
    image: FileRDTO | None = None

    class Config:
        from_attributes = True

