from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_action_dto import CartActionResponseDTO
from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO, CartCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class ClearCartCase(BaseUseCase[CartActionResponseDTO]):
    """
    Use Case для полной очистки корзины пользователя.

    Функциональность:
    - Находит корзину пользователя по cart_id и user_id
    - Удаляет все элементы корзины (force_delete=True)
    - Обнуляет total_price и cart_items в корзине
    - Проверяет права доступа (корзина должна принадлежать пользователю)

    Безопасность:
    - Проверяет, что корзина принадлежит именно текущему пользователю
    - Использует force_delete для полного удаления элементов
    """

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозиториев для работы с данными
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.cart_entity: CartEntity | None = None  # Корзина для очистки

        # Входные данные для обработки
        self.cart_id: int | None = None  # ID корзины для очистки
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь

    async def execute(self, cart_id: int, user: UserWithRelationsRDTO) -> CartActionResponseDTO:
        """
        Основной метод выполнения очистки корзины.

        Args:
            cart_id: ID корзины для очистки
            user: Текущий пользователь

        Returns:
            CartActionResponseDTO: Ответ с очищенной корзиной

        Raises:
            AppExceptionResponse.bad_request: При отсутствии обязательных параметров
                                            или если корзина не найдена/не принадлежит пользователю
        """
        # Сохраняем входные данные в instance переменные
        self.cart_id = cart_id
        self.current_user = user

        # Валидируем входные данные и права доступа к корзине
        await self.validate()

        # Выполняем бизнес-логику очистки корзины
        await self.transform()

        # Дожидаемся обновления через EventHandler
        await self.cart_repository.db.flush()
        await self.cart_repository.db.commit()

        # Получаем обновленную (очищенную) корзину с relationships для возврата
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[
                self.cart_repository.model.user_id == self.current_user.id,
                self.cart_repository.model.id == self.cart_id
            ],
            options=self.cart_repository.default_relationships()
        )

        # Формируем ответ с очищенной корзиной и нулевой общей стоимостью
        return CartActionResponseDTO(
            cart=CartWithRelationsRDTO.from_orm(self.cart_entity),
            cart_items=[],  # Корзина пуста после очистки
            total_price=0.0,  # Общая стоимость очищенной корзины равна нулю
        )

    async def validate(self) -> None:
        """
        Валидация входных данных и проверка прав доступа к корзине.

        Проверяет:
        1. Наличие обязательных параметров (cart_id и user)
        2. Существование корзины с указанным ID
        3. Принадлежность корзины текущему пользователю (безопасность)

        Raises:
            AppExceptionResponse.bad_request: При отсутствии обязательных параметров
                                            или если корзина не найдена/не принадлежит пользователю
        """
        # Проверяем наличие обязательных параметров
        if self.cart_id is None or self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("user_or_cart_id_not_included"))

        # Находим корзину, проверяя одновременно её существование и принадлежность пользователю
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[
                self.cart_repository.model.user_id == self.current_user.id,
                self.cart_repository.model.id == self.cart_id,
            ]
        )

        # Если корзина не найдена или не принадлежит пользователю
        if not self.cart_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_not_found"))

    async def transform(self) -> None:
        """
        Основная бизнес-логика очистки корзины.

        Выполняет следующие операции:
        1. Получает все элементы корзины (включая soft-deleted)
        2. Удаляет все элементы корзины с force_delete=True
        3. Обновляет корзину: обнуляет total_price и cart_items

        Использует force_delete=True для полного удаления элементов корзины,
        так как при очистке корзины элементы должны быть удалены безвозвратно.
        """
        # Получаем все элементы корзины (включая soft-deleted для полной очистки)
        cart_items = await self.cart_item_repository.get_with_filters(
            filters=[
                self.cart_item_repository.model.cart_id == self.cart_entity.id
            ],
            include_deleted_filter=True,  # Включаем soft-deleted элементы
        )

        # Удаляем все элементы корзины с force_delete для полного удаления
        if cart_items:
            for cart_item in cart_items:
                await self.cart_item_repository.delete(cart_item.id, force_delete=True)

        # Обновляем корзину: обнуляем total_price и очищаем cart_items
        cart_dto = CartCDTO.from_orm(self.cart_entity)
        cart_dto.cart_items = None  # Очищаем snapshot элементов корзины
        cart_dto.total_price = Decimal("0.00")  # Обнуляем общую стоимость

        # Сохраняем обновленную корзину
        await self.cart_repository.update(obj=self.cart_entity, dto=cart_dto)