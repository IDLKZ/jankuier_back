from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_action_dto import CartActionResponseDTO
from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.dto.cart_item.cart_item_dto import CartItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity, CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetUserCartCase(BaseUseCase[CartActionResponseDTO]):
    """
    Use Case для получения корзины пользователя.

    Функциональность:
    - Находит существующую корзину пользователя или создает новую
    - Возвращает корзину со всеми связанными данными (элементы, товары, варианты)
    - Поддерживает опциональное обновление snapshot элементов корзины
    - Автоматически создает корзину если она отсутствует

    Особенности:
    - Всегда возвращает корзину (создает если нет)
    - Загружает все relationships через default_relationships()
    - Безопасно работает с несуществующими корзинами
    """

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозитория для работы с корзинами
        self.cart_repository = CartRepository(db)
        self.cart_items_repository = CartItemRepository(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.cart_entity: CartEntity | None = None  # Корзина пользователя
        self.cart_items_entity: List[CartItemEntity] | None = []  # Корзина пользователя

        # Входные данные для обработки
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь
        self.check_cart_items: bool = False  # Флаг необходимости обновления snapshot элементов
        self.total_price:float = 0.00

    async def execute(self, user: UserWithRelationsRDTO, check_cart_items: bool = False) -> CartActionResponseDTO:
        """
        Основной метод получения корзины пользователя.

        Args:
            user: Текущий пользователь, для которого нужно получить корзину
            check_cart_items: Флаг обновления snapshot элементов корзины (по умолчанию False)

        Returns:
            CartActionResponseDTO: Ответ с корзиной, элементами и общей стоимостью

        Raises:
            AppExceptionResponse.bad_request: При отсутствии пользователя или ошибке создания корзины

        Note:
            Параметр check_cart_items включает принудительное обновление snapshot элементов корзины.
            Полезно когда нужно синхронизировать данные корзины с актуальными данными товаров.
        """
        # Сохраняем входные данные в instance переменные
        self.current_user = user
        self.check_cart_items = check_cart_items

        # Валидируем пользователя и находим/создаем корзину
        await self.validate()

        # Выполняем валидацию актуальности товаров и вариантов
        await self.transform()

        # Получаем обновленную корзину после возможных изменений
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id],
            options=self.cart_repository.default_relationships()
        )
        if self.cart_entity:
            self.cart_items_entity = await self.cart_items_repository.get_with_filters(
                filters=[self.cart_items_repository.model.cart_id == self.cart_entity.id],
                options=self.cart_items_repository.default_relationships(),
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
        Валидация пользователя и обеспечение существования корзины.

        Проверяет:
        1. Наличие пользователя
        2. Существование корзины пользователя
        3. Автоматически создает корзину если она отсутствует

        Raises:
            AppExceptionResponse.bad_request: При отсутствии пользователя или ошибке создания корзины
        """
        # Проверяем наличие пользователя
        if self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("user_not_included"))

        # Ищем существующую корзину пользователя
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id],
            options=self.cart_repository.default_relationships()
        )

        # Если корзины нет - создаем новую
        if not self.cart_entity:
            await self.cart_repository.create(CartEntity(user_id=self.current_user.id))
            self.cart_entity = await self.cart_repository.get_first_with_filters(
                filters=[self.cart_repository.model.user_id == self.current_user.id],
                options=self.cart_repository.default_relationships()
            )

        # Проверяем, что корзина успешно создана/найдена
        if not self.cart_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_not_found"))

        # Загружаем элементы корзины
        self.cart_items_entity = await self.cart_items_repository.get_with_filters(
            filters=[self.cart_items_repository.model.cart_id == self.cart_entity.id],
            options=self.cart_items_repository.default_relationships()
        )

        # Вычисляем текущую сумму элементов для сравнения
        calculated_total = 0.0
        for cart_item_entity in self.cart_items_entity:
            calculated_total += float(cart_item_entity.total_price)

        # Если суммы не совпадают - включаем проверку элементов корзины
        if calculated_total != float(self.cart_entity.total_price):
            self.check_cart_items = True

        # Сохраняем актуальную сумму для возврата
        self.total_price = float(self.cart_entity.total_price)



    async def transform(self) -> None:
        """
        Валидация и синхронизация товаров и вариантов в корзине.

        Логика обработки:
        1. Удаление: только если товар/вариант неактивен или не найден
        2. Обновление цен: если base_price или price_delta изменились
        3. Автоматический пересчет суммы происходит через EventHandler при update/delete

        Условия удаления:
        - product.is_active == False ИЛИ product == None
        - variant.is_active == False ИЛИ variant == None (если variant_id указан)

        Условия обновления:
        - product.base_price != cart_item.product_price
        - variant.price_delta != cart_item.delta_price (если есть вариант)
        """
        if self.check_cart_items:
            from app.adapters.dto.cart_item.cart_item_dto import CartItemCDTO
            from decimal import Decimal

            items_to_remove = []  # Список элементов для удаления
            items_to_update = []  # Список элементов для обновления

            # Итерируемся по всем элементам корзины
            for cart_item in self.cart_items_entity:
                should_remove = False
                should_update = False
                updated_product_price = None
                updated_delta_price = None

                # Получаем связанные данные
                product = cart_item.product
                variant = cart_item.variant

                # Проверяем наличие продукта
                if not product:
                    should_remove = True
                else:
                    # Проверяем активность продукта
                    if not product.is_active:
                        should_remove = True
                    else:
                        # Проверяем и обновляем цену продукта
                        if product.base_price != cart_item.product_price:
                            should_update = True
                            updated_product_price = product.base_price

                        # Обработка варианта (если указан variant_id)
                        if cart_item.variant_id:
                            if not variant:
                                # Вариант не найден - удаляем
                                should_remove = True
                            else:
                                # Проверяем активность варианта
                                if not variant.is_active:
                                    should_remove = True
                                else:
                                    # Проверяем и обновляем price_delta
                                    if variant.price_delta != cart_item.delta_price:
                                        should_update = True
                                        updated_delta_price = variant.price_delta

                # Определяем действие
                if should_remove:
                    items_to_remove.append(cart_item)
                elif should_update:
                    items_to_update.append({
                        'cart_item': cart_item,
                        'product_price': updated_product_price,
                        'delta_price': updated_delta_price
                    })

            # Удаляем неактивные элементы корзины
            for item in items_to_remove:
                await self.cart_items_repository.delete(item.id, force_delete=True)
                # Убираем из локального списка
                self.cart_items_entity.remove(item)

            # Обновляем цены элементов корзины
            for update_data in items_to_update:
                cart_item = update_data['cart_item']

                # Создаем DTO для обновления
                cart_item_dto = CartItemCDTO.from_orm(cart_item)

                # Обновляем цены если они изменились
                if update_data['product_price'] is not None:
                    cart_item_dto.product_price = update_data['product_price']

                if update_data['delta_price'] is not None:
                    cart_item_dto.delta_price = update_data['delta_price']

                # Сохраняем обновления (пересчет unit_price и total_price происходит автоматически)
                await self.cart_items_repository.update(obj=cart_item, dto=cart_item_dto)

            # Пересчет общей суммы корзины происходит автоматически через CartItemEventHandler



