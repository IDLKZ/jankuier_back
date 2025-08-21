from datetime import date

from fastapi import Form, HTTPException
from typing import Optional

from pydantic import ValidationError
from app.adapters.dto.user.user_dto import UserCDTO
from app.adapters.dto.product.product_dto import ProductCDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantCDTO
from app.adapters.dto.product_category.product_category_dto import ProductCategoryCDTO


class FormParserHelper:
    @staticmethod
    def parse_user_dto_from_form(
        role_id: Optional[int] = Form(None, description="ID роли"),
        image_id: Optional[int] = Form(None, description="ID изображения"),
        region_id: Optional[int] = Form(None, description="ID региона"),
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
    ) -> UserCDTO:
        """
        Парсит `FormData` и возвращает `UserCDTO`.

        :return: Экземпляр `UserCDTO`
        """
        return UserCDTO(
            role_id=role_id,
            image_id=image_id,
            region_id=region_id,
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
