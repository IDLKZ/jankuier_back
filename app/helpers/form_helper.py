from datetime import date, time, datetime
from decimal import Decimal

from fastapi import Form, HTTPException
from typing import Optional

from pydantic import ValidationError
from app.adapters.dto.user.user_dto import UserCDTO
from app.adapters.dto.product.product_dto import ProductCDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantCDTO
from app.adapters.dto.product_category.product_category_dto import ProductCategoryCDTO
from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryCDTO
from app.adapters.dto.field.field_dto import FieldCDTO
from app.adapters.dto.field_party.field_party_dto import FieldPartyCDTO
from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import FieldPartyScheduleSettingsCDTO
from app.adapters.dto.field_party_schedule.field_party_schedule_dto import FieldPartyScheduleCDTO
from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryCDTO
from app.adapters.dto.academy.academy_dto import AcademyCDTO
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupCDTO
from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import AcademyGroupScheduleCDTO
from app.adapters.dto.academy_gallery.academy_gallery_dto import AcademyGalleryCDTO
from app.adapters.dto.academy_material.academy_material_dto import AcademyMaterialCDTO, AcademyMaterialUpdateDTO
from app.adapters.dto.student.student_dto import StudentCDTO, StudentUpdateDTO
from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
    RequestToAcademyGroupCDTO, 
    RequestToAcademyGroupUpdateDTO,
    RequestToAcademyGroupBulkUpdateDTO,
)
from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialCDTO,
    RequestMaterialUpdateDTO,
    RequestMaterialBulkCDTO,
)
from app.adapters.dto.academy_group_student.academy_group_student_dto import (
    AcademyGroupStudentCDTO,
    AcademyGroupStudentUpdateDTO,
    AcademyGroupStudentBulkCDTO,
    AcademyGroupStudentBulkUpdateDTO,
)
from app.adapters.dto.cart.cart_dto import (
    CartCDTO,
    CartUpdateDTO,
    CartCalculateTotalDTO,
)
from app.adapters.dto.cart_item.cart_item_dto import (
    CartItemCDTO,
    CartItemUpdateDTO,
    CartItemBulkCDTO,
    CartItemBulkUpdateQtyDTO,
)
from app.adapters.dto.auth.register_dto import UpdateProfileDTO


class FormParserHelper:
    @staticmethod
    def parse_user_dto_from_form(
        role_id: Optional[int] = Form(None, description="ID роли"),
        image_id: Optional[int] = Form(None, description="ID изображения"),
        # region_id: Optional[int] = Form(None, description="ID региона"),
        first_name: str = Form(..., description="Имя"),
        last_name: str = Form(..., description="Фамилия"),
        patronomic: Optional[str] = Form(None, description="Отчество"),
        email: str = Form(..., description="Электронная почта"),
        phone: str = Form(..., description="Телефон"),
        username: str = Form(..., description="Уникальное имя пользователя"),
        sex: int = Form(
            ..., description="Пол (0 - не указан, 1 - мужской, 2 - женский)"
        ),
        iin: Optional[str] = Form(None, description="ИИН"),
        birthdate: date = Form(..., description="Дата рождения"),
        is_active: bool = Form(False, description="Активен"),
        is_verified: bool = Form(False, description="Подтвержден"),
        password_hash: str = Form(..., description="Подтвержден"),
    ) -> UserCDTO:
        """
        Парсит `FormData` и возвращает `UserCDTO`.

        :return: Экземпляр `UserCDTO`
        """
        return UserCDTO(
            role_id=role_id,
            image_id=image_id,
            # region_id=region_id,
            first_name=first_name,
            last_name=last_name,
            patronomic=patronomic,
            email=email,
            phone=phone,
            username=username,
            sex=sex,
            iin=iin,
            birthdate=birthdate,
            is_active=is_active,
            is_verified=is_verified,
            password_hash=password_hash,
        )

    @staticmethod
    def parse_product_dto_from_form(
        image_id: Optional[int] = Form(None, description="ID главного изображения товара"),
        city_id: Optional[int] = Form(None, description="ID города"),
        category_id: Optional[int] = Form(None, description="ID категории товара"),
        title_ru: str = Form(..., description="Название товара на русском"),
        title_kk: Optional[str] = Form(None, description="Название товара на казахском"),
        title_en: Optional[str] = Form(None, description="Название товара на английском"),
        description_ru: Optional[str] = Form(None, description="Описание товара на русском"),
        description_kk: Optional[str] = Form(None, description="Описание товара на казахском"),
        description_en: Optional[str] = Form(None, description="Описание товара на английском"),
        value: str = Form(..., description="Уникальное значение товара"),
        sku: str = Form(..., description="SKU товара"),
        base_price: float = Form(..., description="Базовая цена товара"),
        old_price: Optional[float] = Form(None, description="Старая цена товара"),
        gender: int = Form(..., description="Пол: 0-унисекс, 1-мужской, 2-женский"),
        is_for_children: bool = Form(False, description="Товар для детей"),
        is_recommended: bool = Form(False, description="Рекомендованный товар"),
        is_active: bool = Form(True, description="Флаг активности товара"),
    ) -> ProductCDTO:
        return ProductCDTO(
            image_id=image_id,
            city_id=city_id,
            category_id=category_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=value,
            sku=sku,
            base_price=base_price,
            old_price=old_price,
            gender=gender,
            is_for_children=is_for_children,
            is_recommended=is_recommended,
            is_active=is_active,
        )

    @staticmethod
    def parse_product_variant_dto_from_form(
        product_id: int = Form(..., description="ID товара"),
        image_id: Optional[int] = Form(None, description="ID изображения варианта"),
        city_id: Optional[int] = Form(None, description="ID города"),
        title_ru: str = Form(..., description="Название варианта на русском"),
        title_kk: Optional[str] = Form(None, description="Название варианта на казахском"),
        title_en: Optional[str] = Form(None, description="Название варианта на английском"),
        value: str = Form(..., description="Уникальное значение варианта"),
        sku: Optional[str] = Form(None, description="SKU варианта товара"),
        price_delta: Optional[float] = Form(None, description="Изменение цены относительно базовой"),
        stock: int = Form(..., description="Количество на складе"),
        is_active: bool = Form(True, description="Флаг активности варианта"),
        is_default: bool = Form(False, description="Вариант по умолчанию"),
    ) -> ProductVariantCDTO:
        return ProductVariantCDTO(
            product_id=product_id,
            image_id=image_id,
            city_id=city_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            value=value,
            sku=sku,
            price_delta=price_delta,
            stock=stock,
            is_active=is_active,
            is_default=is_default,
        )

    @staticmethod
    def parse_product_category_dto_from_form(
        image_id: Optional[int] = Form(None, description="ID изображения категории"),
        title_ru: str = Form(..., description="Название категории на русском"),
        title_kk: Optional[str] = Form(None, description="Название категории на казахском"),
        title_en: Optional[str] = Form(None, description="Название категории на английском"),
        description_ru: Optional[str] = Form(None, description="Описание категории на русском"),
        description_kk: Optional[str] = Form(None, description="Описание категории на казахском"),
        description_en: Optional[str] = Form(None, description="Описание категории на английском"),
        value: str = Form(..., description="Уникальное значение категории"),
        is_active: bool = Form(True, description="Флаг активности категории"),
    ) -> ProductCategoryCDTO:
        return ProductCategoryCDTO(
            image_id=image_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=value,
            is_active=is_active,
        )

    @staticmethod
    def parse_product_gallery_dto_from_form(
        product_id: int = Form(..., description="ID товара"),
        variant_id: Optional[int] = Form(None, description="ID варианта товара"),
        file_id: Optional[int] = Form(None, description="ID файла изображения"),
    ) -> ProductGalleryCDTO:
        return ProductGalleryCDTO(
            product_id=product_id,
            variant_id=variant_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_field_dto_from_form(
        image_id: Optional[int] = Form(None, description="ID главного изображения поля"),
        city_id: Optional[int] = Form(None, description="ID города"),
        title_ru: str = Form(..., description="Название поля на русском"),
        title_kk: Optional[str] = Form(None, description="Название поля на казахском"),
        title_en: Optional[str] = Form(None, description="Название поля на английском"),
        description_ru: Optional[str] = Form(None, description="Описание поля на русском"),
        description_kk: Optional[str] = Form(None, description="Описание поля на казахском"),
        description_en: Optional[str] = Form(None, description="Описание поля на английском"),
        value: str = Form(..., description="Уникальное значение поля"),
        address_ru: Optional[str] = Form(None, description="Адрес на русском"),
        address_en: Optional[str] = Form(None, description="Адрес на английском"),
        address_kk: Optional[str] = Form(None, description="Адрес на казахском"),
        latitude: Optional[str] = Form(None, description="Широта"),
        longitude: Optional[str] = Form(None, description="Долгота"),
        is_active: bool = Form(True, description="Флаг активности поля"),
        has_cover: bool = Form(False, description="Наличие крыши"),
        phone: Optional[str] = Form(None, description="Телефон"),
        additional_phone: Optional[str] = Form(None, description="Дополнительный телефон"),
        email: Optional[str] = Form(None, description="Email"),
        whatsapp: Optional[str] = Form(None, description="WhatsApp"),
        telegram: Optional[str] = Form(None, description="Telegram"),
        instagram: Optional[str] = Form(None, description="Instagram"),
        tiktok: Optional[str] = Form(None, description="TikTok"),
    ) -> FieldCDTO:
        return FieldCDTO(
            image_id=image_id,
            city_id=city_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=value,
            address_ru=address_ru,
            address_en=address_en,
            address_kk=address_kk,
            latitude=latitude,
            longitude=longitude,
            is_active=is_active,
            has_cover=has_cover,
            phone=phone,
            additional_phone=additional_phone,
            email=email,
            whatsapp=whatsapp,
            telegram=telegram,
            instagram=instagram,
            tiktok=tiktok,
        )

    @staticmethod
    def parse_field_party_dto_from_form(
        image_id: Optional[int] = Form(None, description="ID изображения площадки"),
        field_id: int = Form(..., description="ID поля"),
        title_ru: str = Form(..., description="Название площадки на русском"),
        title_kk: Optional[str] = Form(None, description="Название площадки на казахском"),
        title_en: Optional[str] = Form(None, description="Название площадки на английском"),
        value: str = Form(..., description="Уникальное значение площадки"),
        person_qty: int = Form(..., description="Количество людей"),
        length_m: int = Form(..., description="Длина в метрах"),
        width_m: int = Form(..., description="Ширина в метрах"),
        deepth_m: Optional[int] = Form(None, description="Глубина в метрах"),
        latitude: Optional[str] = Form(None, description="Широта"),
        longitude: Optional[str] = Form(None, description="Долгота"),
        is_active: bool = Form(True, description="Флаг активности площадки"),
        is_covered: bool = Form(False, description="Наличие крыши"),
        is_default: bool = Form(False, description="Площадка по умолчанию"),
        cover_type: int = Form(..., description="Тип покрытия"),
    ) -> FieldPartyCDTO:
        return FieldPartyCDTO(
            image_id=image_id,
            field_id=field_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            value=value,
            person_qty=person_qty,
            length_m=length_m,
            width_m=width_m,
            deepth_m=deepth_m,
            latitude=latitude,
            longitude=longitude,
            is_active=is_active,
            is_covered=is_covered,
            is_default=is_default,
            cover_type=cover_type,
        )

    @staticmethod
    def parse_field_party_schedule_settings_dto_from_form(
        party_id: int = Form(..., description="ID площадки"),
        active_start_at: date = Form(..., description="Дата начала активности"),
        active_end_at: date = Form(..., description="Дата окончания активности"),
        working_days: str = Form(..., description="Рабочие дни в формате JSON [1,2,3,4,5]"),
        excluded_dates: Optional[str] = Form(None, description="Исключенные даты в формате JSON"),
        working_time: str = Form(..., description="Рабочее время в формате JSON"),
        break_time: str = Form(..., description="Время перерыва в формате JSON"),
        price_per_time: str = Form(..., description="Цены по времени в формате JSON"),
        session_minute_int: int = Form(..., description="Длительность сессии в минутах"),
        break_between_session_int: int = Form(..., description="Перерыв между сессиями в минутах"),
        booked_limit: int = Form(..., description="Лимит бронирований"),
    ) -> FieldPartyScheduleSettingsCDTO:
        import json
        
        # Parse JSON fields
        try:
            working_days_parsed = json.loads(working_days) if working_days else []
            excluded_dates_parsed = json.loads(excluded_dates) if excluded_dates else None
            working_time_parsed = json.loads(working_time) if working_time else {}
            break_time_parsed = json.loads(break_time) if break_time else {}
            price_per_time_parsed = json.loads(price_per_time) if price_per_time else {}
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
        
        return FieldPartyScheduleSettingsCDTO(
            party_id=party_id,
            active_start_at=active_start_at,
            active_end_at=active_end_at,
            working_days=working_days_parsed,
            excluded_dates=excluded_dates_parsed,
            working_time=working_time_parsed,
            break_time=break_time_parsed,
            price_per_time=price_per_time_parsed,
            session_minute_int=session_minute_int,
            break_between_session_int=break_between_session_int,
            booked_limit=booked_limit,
        )

    @staticmethod
    def parse_field_party_schedule_dto_from_form(
        party_id: int = Form(..., description="ID площадки"),
        setting_id: int = Form(..., description="ID настроек расписания"),
        day: date = Form(..., description="Дата"),
        start_at: time = Form(..., description="Время начала"),
        end_at: time = Form(..., description="Время окончания"),
        price: Decimal = Form(..., description="Цена за период"),
        is_booked: bool = Form(False, description="Забронировано"),
        is_paid: bool = Form(False, description="Оплачено"),
    ) -> FieldPartyScheduleCDTO:
        return FieldPartyScheduleCDTO(
            party_id=party_id,
            setting_id=setting_id,
            day=day,
            start_at=start_at,
            end_at=end_at,
            price=price,
            is_booked=is_booked,
            is_paid=is_paid,
        )

    @staticmethod
    def parse_field_gallery_dto_from_form(
        field_id: int = Form(..., description="ID поля"),
        party_id: Optional[int] = Form(None, description="ID площадки (опционально)"),
        file_id: Optional[int] = Form(None, description="ID файла изображения"),
    ) -> FieldGalleryCDTO:
        return FieldGalleryCDTO(
            field_id=field_id,
            party_id=party_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_academy_dto_from_form(
        image_id: Optional[int] = Form(None, description="ID главного изображения академии"),
        city_id: Optional[int] = Form(None, description="ID города"),
        title_ru: str = Form(..., description="Название академии на русском"),
        title_kk: Optional[str] = Form(None, description="Название академии на казахском"),
        title_en: Optional[str] = Form(None, description="Название академии на английском"),
        description_ru: Optional[str] = Form(None, description="Описание академии на русском"),
        description_kk: Optional[str] = Form(None, description="Описание академии на казахском"),
        description_en: Optional[str] = Form(None, description="Описание академии на английском"),
        value: str = Form(..., description="Уникальное значение академии"),
        address_ru: Optional[str] = Form(None, description="Адрес на русском"),
        address_kk: Optional[str] = Form(None, description="Адрес на казахском"),
        address_en: Optional[str] = Form(None, description="Адрес на английском"),
        working_time: str = Form(..., description="Рабочее время в формате JSON"),
        is_active: bool = Form(True, description="Флаг активности академии"),
        gender: int = Form(..., description="Пол: 0-оба, 1-мужской, 2-женский"),
        min_age: int = Form(..., description="Минимальный возраст"),
        max_age: int = Form(..., description="Максимальный возраст"),
        average_price: Optional[Decimal] = Form(None, description="Средняя цена"),
        average_training_time_in_minute: Optional[int] = Form(None, description="Среднее время тренировки в минутах"),
        phone: Optional[str] = Form(None, description="Телефон"),
        additional_phone: Optional[str] = Form(None, description="Дополнительный телефон"),
        email: Optional[str] = Form(None, description="Email"),
        whatsapp: Optional[str] = Form(None, description="WhatsApp"),
        telegram: Optional[str] = Form(None, description="Telegram"),
        instagram: Optional[str] = Form(None, description="Instagram"),
        tik_tok: Optional[str] = Form(None, description="TikTok"),
        site: Optional[str] = Form(None, description="Сайт"),
    ) -> AcademyCDTO:
        import json
        
        # Parse JSON field
        try:
            working_time_parsed = json.loads(working_time) if working_time else {}
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format for working_time: {str(e)}")
        
        return AcademyCDTO(
            image_id=image_id,
            city_id=city_id,
            title_ru=title_ru,
            title_kk=title_kk,
            title_en=title_en,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=value,
            address_ru=address_ru,
            address_kk=address_kk,
            address_en=address_en,
            working_time=working_time_parsed,
            is_active=is_active,
            gender=gender,
            min_age=min_age,
            max_age=max_age,
            average_price=average_price,
            average_training_time_in_minute=average_training_time_in_minute,
            phone=phone,
            additional_phone=additional_phone,
            email=email,
            whatsapp=whatsapp,
            telegram=telegram,
            instagram=instagram,
            tik_tok=tik_tok,
            site=site,
        )

    @staticmethod
    def parse_academy_group_dto_from_form(
        academy_id: int = Form(..., description="ID академии"),
        image_id: Optional[int] = Form(None, description="ID изображения группы"),
        name: str = Form(..., description="Название группы"),
        description_ru: Optional[str] = Form(None, description="Описание группы на русском"),
        description_kk: Optional[str] = Form(None, description="Описание группы на казахском"),
        description_en: Optional[str] = Form(None, description="Описание группы на английском"),
        value: str = Form(..., description="Уникальное значение группы"),
        min_age: int = Form(..., description="Минимальный возраст"),
        max_age: int = Form(..., description="Максимальный возраст"),
        is_active: bool = Form(True, description="Флаг активности группы"),
        is_recruiting: bool = Form(False, description="Идет набор в группу"),
        gender: int = Form(..., description="Пол: 0-оба, 1-мужской, 2-женский"),
        booked_space: int = Form(0, description="Занятых мест"),
        free_space: int = Form(0, description="Свободных мест"),
        price: Optional[Decimal] = Form(None, description="Цена"),
        price_per_ru: Optional[str] = Form(None, description="Описание цены на русском"),
        price_per_kk: Optional[str] = Form(None, description="Описание цены на казахском"),
        price_per_en: Optional[str] = Form(None, description="Описание цены на английском"),
        average_training_time_in_minute: Optional[int] = Form(None, description="Среднее время тренировки в минутах"),
    ) -> AcademyGroupCDTO:
        return AcademyGroupCDTO(
            academy_id=academy_id,
            image_id=image_id,
            name=name,
            description_ru=description_ru,
            description_kk=description_kk,
            description_en=description_en,
            value=value,
            min_age=min_age,
            max_age=max_age,
            is_active=is_active,
            is_recruiting=is_recruiting,
            gender=gender,
            booked_space=booked_space,
            free_space=free_space,
            price=price,
            price_per_ru=price_per_ru,
            price_per_kk=price_per_kk,
            price_per_en=price_per_en,
            average_training_time_in_minute=average_training_time_in_minute,
        )

    @staticmethod
    def parse_academy_group_schedule_dto_from_form(
        group_id: int = Form(..., description="ID группы академии"),
        training_date: date = Form(..., description="Дата тренировки"),
        start_at: time = Form(..., description="Время начала"),
        end_at: time = Form(..., description="Время окончания"),
        reschedule_start_at: Optional[datetime] = Form(None, description="Новое время начала при переносе"),
        reschedule_end_at: Optional[datetime] = Form(None, description="Новое время окончания при переносе"),
        is_active: bool = Form(True, description="Флаг активности расписания"),
        is_canceled: bool = Form(False, description="Тренировка отменена"),
        is_finished: bool = Form(False, description="Тренировка завершена"),
    ) -> AcademyGroupScheduleCDTO:
        return AcademyGroupScheduleCDTO(
            group_id=group_id,
            training_date=training_date,
            start_at=start_at,
            end_at=end_at,
            reschedule_start_at=reschedule_start_at,
            reschedule_end_at=reschedule_end_at,
            is_active=is_active,
            is_canceled=is_canceled,
            is_finished=is_finished,
        )

    @staticmethod
    def parse_academy_gallery_dto_from_form(
        academy_id: int = Form(..., description="ID академии"),
        group_id: Optional[int] = Form(None, description="ID группы (опционально)"),
        file_id: Optional[int] = Form(None, description="ID файла изображения"),
    ) -> AcademyGalleryCDTO:
        return AcademyGalleryCDTO(
            academy_id=academy_id,
            group_id=group_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_academy_material_dto_from_form(
        title: str = Form(..., description="Название материала"),
        academy_id: int = Form(..., description="ID академии"),
        group_id: Optional[int] = Form(None, description="ID группы (опционально)"),
        file_id: Optional[int] = Form(None, description="ID файла материала"),
    ) -> AcademyMaterialCDTO:
        return AcademyMaterialCDTO(
            title=title,
            academy_id=academy_id,
            group_id=group_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_academy_material_update_dto_from_form(
        title: Optional[str] = Form(None, description="Название материала"),
        group_id: Optional[int] = Form(None, description="ID группы"),
        file_id: Optional[int] = Form(None, description="ID файла материала"),
    ) -> AcademyMaterialUpdateDTO:
        return AcademyMaterialUpdateDTO(
            title=title,
            group_id=group_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_student_dto_from_form(
        first_name: str = Form(..., description="Имя"),
        last_name: str = Form(..., description="Фамилия"),
        patronymic: Optional[str] = Form(None, description="Отчество"),
        birthdate: date = Form(..., description="Дата рождения"),
        gender: int = Form(..., description="Пол: 0-оба, 1-мужской, 2-женский"),
        phone: Optional[str] = Form(None, description="Телефон"),
        additional_phone: Optional[str] = Form(None, description="Дополнительный телефон"),
        email: Optional[str] = Form(None, description="Email"),
        info: Optional[str] = Form(None, description="Дополнительная информация"),
        reschedule_end_at: Optional[datetime] = Form(None, description="Дата окончания переноса"),
        created_by: Optional[int] = Form(None, description="ID пользователя, создавшего студента"),
        image_id: Optional[int] = Form(None, description="ID фотографии студента"),
    ) -> StudentCDTO:
        return StudentCDTO(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            birthdate=birthdate,
            gender=gender,
            phone=phone,
            additional_phone=additional_phone,
            email=email,
            info=info,
            reschedule_end_at=reschedule_end_at,
            created_by=created_by,
            image_id=image_id,
        )

    @staticmethod
    def parse_student_update_dto_from_form(
        first_name: Optional[str] = Form(None, description="Имя"),
        last_name: Optional[str] = Form(None, description="Фамилия"),
        patronymic: Optional[str] = Form(None, description="Отчество"),
        birthdate: Optional[date] = Form(None, description="Дата рождения"),
        gender: Optional[int] = Form(None, description="Пол: 0-оба, 1-мужской, 2-женский"),
        phone: Optional[str] = Form(None, description="Телефон"),
        additional_phone: Optional[str] = Form(None, description="Дополнительный телефон"),
        email: Optional[str] = Form(None, description="Email"),
        info: Optional[str] = Form(None, description="Дополнительная информация"),
        reschedule_end_at: Optional[datetime] = Form(None, description="Дата окончания переноса"),
        image_id: Optional[int] = Form(None, description="ID фотографии студента"),
    ) -> StudentUpdateDTO:
        return StudentUpdateDTO(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            birthdate=birthdate,
            gender=gender,
            phone=phone,
            additional_phone=additional_phone,
            email=email,
            info=info,
            reschedule_end_at=reschedule_end_at,
            image_id=image_id,
        )

    @staticmethod
    def parse_request_to_academy_group_dto_from_form(
        student_id: int = Form(..., description="ID студента"),
        group_id: int = Form(..., description="ID группы академии"),
        status: int = Form(0, description="Статус заявки: 0-не просмотрена, 1-принята, -1-отклонена"),
        checked_by: Optional[int] = Form(None, description="ID пользователя, проверившего заявку"),
        info: Optional[str] = Form(None, description="Дополнительная информация о заявке"),
    ) -> RequestToAcademyGroupCDTO:
        return RequestToAcademyGroupCDTO(
            student_id=student_id,
            group_id=group_id,
            status=status,
            checked_by=checked_by,
            info=info,
        )

    @staticmethod
    def parse_request_to_academy_group_update_dto_from_form(
        status: Optional[int] = Form(None, description="Статус заявки: 0-не просмотрена, 1-принята, -1-отклонена"),
        checked_by: Optional[int] = Form(None, description="ID пользователя, проверившего заявку"),
        info: Optional[str] = Form(None, description="Дополнительная информация о заявке"),
    ) -> RequestToAcademyGroupUpdateDTO:
        return RequestToAcademyGroupUpdateDTO(
            status=status,
            checked_by=checked_by,
            info=info,
        )

    @staticmethod
    def parse_request_to_academy_group_bulk_update_dto_from_form(
        request_ids: str = Form(..., description="ID заявок через запятую"),
        status: int = Form(..., description="Статус заявок: 0-не просмотрена, 1-принята, -1-отклонена"),
        checked_by: Optional[int] = Form(None, description="ID пользователя, проверившего заявки"),
    ) -> RequestToAcademyGroupBulkUpdateDTO:
        # Парсинг списка ID из строки
        try:
            parsed_ids = [int(id.strip()) for id in request_ids.split(",") if id.strip()]
        except ValueError:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid request_ids format")
        
        return RequestToAcademyGroupBulkUpdateDTO(
            request_ids=parsed_ids,
            status=status,
            checked_by=checked_by,
        )

    @staticmethod
    def parse_request_material_dto_from_form(
        title: str = Form(..., description="Название материала запроса"),
        request_id: int = Form(..., description="ID заявки в группу"),
        student_id: int = Form(..., description="ID студента"),
        file_id: Optional[int] = Form(None, description="ID файла материала"),
    ) -> RequestMaterialCDTO:
        return RequestMaterialCDTO(
            title=title,
            request_id=request_id,
            student_id=student_id,
            file_id=file_id,
        )

    @staticmethod
    def parse_request_material_update_dto_from_form(
        title: Optional[str] = Form(None, description="Название материала запроса"),
        file_id: Optional[int] = Form(None, description="ID файла материала"),
    ) -> RequestMaterialUpdateDTO:
        return RequestMaterialUpdateDTO(
            title=title,
            file_id=file_id,
        )

    @staticmethod
    def parse_request_material_bulk_dto_from_form(
        request_id: int = Form(..., description="ID заявки в группу"),
        student_id: int = Form(..., description="ID студента"),
        materials: str = Form(..., description="Материалы в JSON формате"),
    ) -> RequestMaterialBulkCDTO:
        # Парсинг JSON из строки
        try:
            import json
            parsed_materials = json.loads(materials) if materials else []
        except (json.JSONDecodeError, ValueError):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid materials JSON format")
        
        return RequestMaterialBulkCDTO(
            request_id=request_id,
            student_id=student_id,
            materials=parsed_materials,
        )

    @staticmethod
    def parse_academy_group_student_dto_from_form(
        student_id: int = Form(..., description="ID студента"),
        group_id: int = Form(..., description="ID группы академии"),
        request_id: Optional[int] = Form(None, description="ID заявки (если студент был добавлен через заявку)"),
        is_active: bool = Form(True, description="Активность студента в группе"),
        info: Optional[str] = Form(None, description="Дополнительная информация"),
    ) -> AcademyGroupStudentCDTO:
        return AcademyGroupStudentCDTO(
            student_id=student_id,
            group_id=group_id,
            request_id=request_id,
            is_active=is_active,
            info=info,
        )

    @staticmethod
    def parse_academy_group_student_update_dto_from_form(
        is_active: Optional[bool] = Form(None, description="Активность студента в группе"),
        info: Optional[str] = Form(None, description="Дополнительная информация"),
    ) -> AcademyGroupStudentUpdateDTO:
        return AcademyGroupStudentUpdateDTO(
            is_active=is_active,
            info=info,
        )

    @staticmethod
    def parse_academy_group_student_bulk_dto_from_form(
        group_id: int = Form(..., description="ID группы академии"),
        students: str = Form(..., description="Студенты в JSON формате"),
    ) -> AcademyGroupStudentBulkCDTO:
        # Парсинг JSON из строки
        try:
            import json
            parsed_students = json.loads(students) if students else []
        except (json.JSONDecodeError, ValueError):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid students JSON format")
        
        return AcademyGroupStudentBulkCDTO(
            group_id=group_id,
            students=parsed_students,
        )

    @staticmethod
    def parse_academy_group_student_bulk_update_dto_from_form(
        student_ids: str = Form(..., description="ID студентов через запятую"),
        group_id: int = Form(..., description="ID группы академии"),
        is_active: bool = Form(..., description="Активность студентов в группе"),
    ) -> AcademyGroupStudentBulkUpdateDTO:
        # Парсинг списка ID из строки
        try:
            parsed_ids = [int(id.strip()) for id in student_ids.split(",") if id.strip()]
        except ValueError:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid student_ids format")
        
        return AcademyGroupStudentBulkUpdateDTO(
            student_ids=parsed_ids,
            group_id=group_id,
            is_active=is_active,
        )

    @staticmethod
    def parse_cart_dto_from_form(
        user_id: int = Form(..., description="ID пользователя"),
        total_price: float = Form(0.0, description="Общая стоимость корзины"),
        cart_items: Optional[str] = Form(None, description="Товары в корзине в JSON формате"),
    ) -> CartCDTO:
        # Парсинг JSON из строки если передан
        parsed_cart_items = None
        if cart_items:
            try:
                import json
                parsed_cart_items = json.loads(cart_items)
            except (json.JSONDecodeError, ValueError):
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="Invalid cart_items JSON format")
        
        return CartCDTO(
            user_id=user_id,
            total_price=total_price,
            cart_items=parsed_cart_items,
        )

    @staticmethod
    def parse_cart_update_dto_from_form(
        total_price: Optional[float] = Form(None, description="Общая стоимость корзины"),
        cart_items: Optional[str] = Form(None, description="Товары в корзине в JSON формате"),
    ) -> CartUpdateDTO:
        # Парсинг JSON из строки если передан
        parsed_cart_items = None
        if cart_items:
            try:
                import json
                parsed_cart_items = json.loads(cart_items)
            except (json.JSONDecodeError, ValueError):
                from fastapi import HTTPException
                raise HTTPException(status_code=400, detail="Invalid cart_items JSON format")
        
        return CartUpdateDTO(
            total_price=total_price,
            cart_items=parsed_cart_items,
        )

    @staticmethod
    def parse_cart_calculate_total_dto_from_form(
        cart_id: int = Form(..., description="ID корзины"),
    ) -> CartCalculateTotalDTO:
        return CartCalculateTotalDTO(
            cart_id=cart_id,
        )

    @staticmethod
    def parse_cart_item_dto_from_form(
        cart_id: int = Form(..., description="ID корзины"),
        product_id: int = Form(..., description="ID товара"),
        variant_id: Optional[int] = Form(None, description="ID варианта товара"),
        qty: int = Form(..., description="Количество товара"),
        sku: Optional[str] = Form(None, description="Артикул товара"),
        product_price: float = Form(..., description="Базовая цена товара"),
        delta_price: float = Form(0.0, description="Дельта цены (надбавка/скидка)"),
        unit_price: float = Form(..., description="Цена за единицу"),
        total_price: float = Form(..., description="Общая стоимость"),
    ) -> CartItemCDTO:
        return CartItemCDTO(
            cart_id=cart_id,
            product_id=product_id,
            variant_id=variant_id,
            qty=qty,
            sku=sku,
            product_price=product_price,
            delta_price=delta_price,
            unit_price=unit_price,
            total_price=total_price,
        )

    @staticmethod
    def parse_cart_item_update_dto_from_form(
        qty: Optional[int] = Form(None, description="Количество товара"),
        delta_price: Optional[float] = Form(None, description="Дельта цены"),
    ) -> CartItemUpdateDTO:
        return CartItemUpdateDTO(
            qty=qty,
            delta_price=delta_price,
        )

    @staticmethod
    def parse_cart_item_bulk_dto_from_form(
        cart_id: int = Form(..., description="ID корзины"),
        items: str = Form(..., description="Товары в JSON формате"),
    ) -> CartItemBulkCDTO:
        # Парсинг JSON из строки
        try:
            import json
            parsed_items = json.loads(items) if items else []
        except (json.JSONDecodeError, ValueError):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid items JSON format")
        
        return CartItemBulkCDTO(
            cart_id=cart_id,
            items=parsed_items,
        )

    @staticmethod
    def parse_cart_item_bulk_update_qty_dto_from_form(
        cart_item_updates: str = Form(..., description="Обновления товаров в JSON формате"),
    ) -> CartItemBulkUpdateQtyDTO:
        # Парсинг JSON из строки
        try:
            import json
            parsed_updates = json.loads(cart_item_updates) if cart_item_updates else []
        except (json.JSONDecodeError, ValueError):
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Invalid cart_item_updates JSON format")
        
        return CartItemBulkUpdateQtyDTO(
            cart_item_updates=parsed_updates,
        )

    @staticmethod
    def parse_update_profile_dto_from_form(
        email: str = Form(..., description="Email"),
        phone: str = Form(..., description="Телефон"),
        iin: Optional[str] = Form(None, description="ИИН"),
        first_name: str = Form(..., description="Имя"),
        last_name: str = Form(..., description="Фамилия"),
        patronymic: Optional[str] = Form(None, description="Отчество"),
    ) -> UpdateProfileDTO:
        return UpdateProfileDTO(
            email=email,
            phone=phone,
            iin=iin,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )
