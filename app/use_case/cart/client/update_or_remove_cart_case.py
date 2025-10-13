from decimal import Decimal
from typing import List

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_action_dto import UpdateOrRemoveFromCartDTO, CartActionResponseDTO
from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.dto.cart_item.cart_item_dto import CartItemCDTO, CartItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity, CartItemEntity, ProductEntity, ProductVariantEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateOrRemoveCartCase(BaseUseCase[CartActionResponseDTO]):
    """
    Use Case для обновления количества или удаления товара из корзины пользователя.

    Функциональность:
    - Находит существующий элемент корзины по product_id и variant_id
    - Обновляет количество товара в корзине (updated_qty)
    - Удаляет товар из корзины полностью (remove_completely=True или updated_qty=0)
    - Проверяет stock при обновлении количества
    - Валидирует существование товара и варианта

    Поддерживает два режима работы:
    1. Обновление количества: устанавливает новое количество (updated_qty)
    2. Удаление: полностью удаляет элемент из корзины
    """

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозиториев для работы с данными
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
        self.product_item_repository = ProductVariantRepository(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.cart_entity: CartEntity | None = None  # Корзина пользователя
        self.cart_item_entity: CartItemEntity | None = None  # Существующий элемент корзины для обновления/удаления
        self.current_product: ProductEntity | None = None  # Товар для обновления/удаления
        self.current_product_variant_entity: ProductVariantEntity | None = None  # Вариант товара (если есть)
        self.cart_items_entity: List[CartItemEntity] | None = []  # Корзина пользователя
        # Входные данные для обработки
        self.dto: UpdateOrRemoveFromCartDTO | None = None  # DTO с данными об обновлении/удалении
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь
        self.is_remove: bool = False  # Флаг режима удаления

    async def execute(self, dto: UpdateOrRemoveFromCartDTO, user: UserWithRelationsRDTO) -> CartActionResponseDTO:
        """
        Основной метод выполнения обновления/удаления товара в корзине.

        Args:
            dto: DTO с данными об обновлении (product_id, variant_id, updated_qty, remove_completely)
            user: Текущий пользователь

        Returns:
            CartActionResponseDTO: Ответ с корзиной, элементами и общей стоимостью

        Raises:
            AppExceptionResponse.bad_request: При ошибках валидации или если элемент корзины не найден
        """
        # Сохраняем входные данные в instance переменные
        self.dto = dto
        self.current_user = user

        # Валидируем входные данные и существование товара
        await self.validate()

        # Выполняем бизнес-логику обновления/удаления из корзины
        await self.transform()

        # Получаем обновленную корзину с relationships для возврата
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id],
            options=self.cart_repository.default_relationships()
        )

        if self.cart_entity:
            self.cart_items_entity = await self.cart_item_repository.get_with_filters(
                filters=[self.cart_item_repository.model.cart_id == self.cart_entity.id],
                options=self.cart_item_repository.default_relationships(),
                order_by="id",
                order_direction="desc"
            )

        # Вычисляем общую стоимость корзины вручную
        calculated_total_price = 0.0
        cart_items_dto = []
        if self.cart_items_entity:
            for cart_item in self.cart_items_entity:
                cart_items_dto.append(CartItemWithRelationsRDTO.from_orm(cart_item))
                calculated_total_price += float(cart_item.total_price)

        # Формируем ответ с актуальными данными и рассчитанной общей стоимостью
        return CartActionResponseDTO(
            cart=CartWithRelationsRDTO.from_orm(self.cart_entity),
            cart_items=cart_items_dto,
            total_price=calculated_total_price,
        )

    async def validate(self) -> None:
        """
        Валидация входных данных и определение режима работы.

        Проверяет:
        1. Наличие обязательных параметров (dto и user)
        2. Существование товара в базе данных
        3. Если указан variant_id - существование и принадлежность варианта товару
        4. Определяет режим работы (обновление или удаление) на основе параметров

        Устанавливает флаг self.is_remove в True если:
        - remove_completely = True ИЛИ
        - updated_qty = 0

        Raises:
            AppExceptionResponse.bad_request: При отсутствии обязательных параметров,
                                            несуществующем товаре или варианте
        """
        # Проверяем наличие обязательных параметров
        if self.dto is None or self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("user_or_dto_not_included"))

        # Получаем и проверяем существование товара
        self.current_product = await self.product_repository.get(self.dto.product_id)
        if not self.current_product:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_not_found"))

        # Если указан variant_id, проверяем вариант товара
        if self.dto.variant_id:
            # Получаем вариант товара, который принадлежит указанному продукту
            self.current_product_variant_entity = await self.product_item_repository.get_first_with_filters(
                filters=[
                    and_(
                        self.product_item_repository.model.product_id == self.current_product.id,
                        self.product_item_repository.model.id == self.dto.variant_id
                    )
                ]
            )
            if not self.current_product_variant_entity:
                raise AppExceptionResponse.bad_request(message=i18n.gettext("product_variant_not_found"))

        # Определяем режим работы: удаление или обновление
        if self.dto.remove_completely is True or self.dto.updated_qty == 0:
            self.is_remove = True

    async def transform(self) -> None:
        """
        Основная бизнес-логика обновления/удаления товара из корзины.

        Выполняет следующие операции:
        1. Находит корзину пользователя (создает если отсутствует)
        2. Ищет существующий элемент корзины с указанным product_id и variant_id
        3. В зависимости от режима:
           - Удаляет элемент корзины (force_delete=True)
           - Обновляет количество с проверкой stock

        Для обновления количества:
        - Устанавливает новое количество (не добавляет к существующему)
        - Проверяет доступность stock
        - Обновляет delta_price актуальным значением из варианта

        Raises:
            AppExceptionResponse.bad_request: При отсутствии корзины, элемента корзины
                                            или превышении доступного stock
        """
        # Ищем существующую корзину пользователя
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id]
        )

        # Если корзины нет - создаем новую (на случай, если пользователь пытается обновить несуществующую корзину)
        if not self.cart_entity:
            await self.cart_repository.create(CartEntity(user_id=self.current_user.id))
            self.cart_entity = await self.cart_repository.get_first_with_filters(
                filters=[self.cart_repository.model.user_id == self.current_user.id]
            )

        # Проверяем, что корзина успешно создана/найдена
        if not self.cart_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_not_found"))

        # Ищем существующий элемент корзины с таким же product_id и variant_id
        # Учитываем, что variant_id может быть None (товар без вариантов)
        self.cart_item_entity = await self.cart_item_repository.get_first_with_filters(
            filters=[
                and_(
                    self.cart_item_repository.model.cart_id == self.cart_entity.id,
                    self.cart_item_repository.model.product_id == self.current_product.id,
                    (
                        self.cart_item_repository.model.variant_id == self.current_product_variant_entity.id
                        if self.current_product_variant_entity
                        else self.cart_item_repository.model.variant_id.is_(None)
                    )
                )
            ]
        )

        # Элемент корзины должен существовать для обновления/удаления
        if not self.cart_item_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_item_not_found"))

        # Режим удаления: полностью удаляем элемент из корзины
        if self.is_remove:
            await self.cart_item_repository.delete(self.cart_item_entity.id, force_delete=True)

        # Режим обновления: устанавливаем новое количество
        else:
            # Создаем DTO из существующего элемента для обновления
            cdto = CartItemCDTO.from_orm(self.cart_item_entity)
            cdto.qty = self.dto.updated_qty  # Устанавливаем новое количество (не добавляем!)

            # Проверяем, что новое количество не превышает доступный stock
            available_stock = (
                self.current_product_variant_entity.stock
                if self.current_product_variant_entity
                else self.current_product.stock
            )
            if cdto.qty > available_stock:
                raise AppExceptionResponse.bad_request(message=i18n.gettext("product_not_available"))

            # Обновляем delta_price актуальным значением из варианта
            if self.current_product_variant_entity:
                cdto.delta_price = self.current_product_variant_entity.price_delta
            else:
                cdto.delta_price = Decimal("0.00")

            # Сохраняем обновленный элемент корзины
            await self.cart_item_repository.update(obj=self.cart_item_entity, dto=cdto)