import json
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartCDTO, CartRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateCartCase(BaseUseCase[CartRDTO]):
    """
    Класс Use Case для создания новой корзины.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - Репозиторий `UserRepository` для проверки существования пользователя.
        - DTO `CartCDTO` для входных данных.
        - DTO `CartRDTO` для возврата данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.
        user_repository (UserRepository): Репозиторий для работы с пользователями.
        model (CartEntity | None): Созданная модель корзины.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartRepository(db)
        self.user_repository = UserRepository(db)
        self.model: CartEntity | None = None

    async def execute(self, dto: CartCDTO) -> CartRDTO:
        """
        Выполняет операцию создания корзины.

        Args:
            dto (CartCDTO): Данные для создания корзины.

        Returns:
            CartRDTO: Созданная корзина.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        model = await self.repository.create(self.model)
        return CartRDTO.from_orm(model)

    async def validate(self, dto: CartCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (CartCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Проверка, что у пользователя нет активной корзины
        existing_cart = await self.repository.get_first_with_filters(
            filters=[self.repository.model.user_id == dto.user_id],
            include_deleted_filter=True,
        )
        if existing_cart:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_already_exists")
            )

        # Валидация общей стоимости
        if dto.total_price < Decimal('0'):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_total_calculation_error")
            )

        # Валидация JSON данных корзины (если указаны)
        if dto.cart_items:
            self._validate_cart_items_json(dto.cart_items)

    def _validate_cart_items_json(self, cart_items: any) -> None:
        """
        Валидация JSON данных товаров корзины.

        Args:
            cart_items: JSON данные товаров корзины.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        try:
            if isinstance(cart_items, str):
                parsed_items = json.loads(cart_items)
            elif isinstance(cart_items, (dict, list)):
                parsed_items = cart_items
            else:
                raise ValueError("Invalid JSON format")
            
            # Дополнительная валидация структуры товаров (если нужно)
            if isinstance(parsed_items, list):
                for item in parsed_items:
                    if not isinstance(item, dict):
                        raise ValueError("Each cart item must be an object")
                    # Можно добавить проверки обязательных полей товара
                    
        except (json.JSONDecodeError, ValueError):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_items_invalid_format")
            )

    async def transform(self, dto: CartCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (CartCDTO): Данные для преобразования.
        """
        # Если cart_items не указаны, создаем пустой массив
        if not dto.cart_items:
            dto.cart_items = []

        self.model = CartEntity(**dto.dict())