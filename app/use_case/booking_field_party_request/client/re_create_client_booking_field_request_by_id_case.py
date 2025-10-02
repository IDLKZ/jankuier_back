import traceback
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_create_request_dto import \
    CreateBookingFieldPartyResponseDTO, CreateBookingFieldPartyRequestDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestCDTO,
    BookingFieldPartyRequestWithRelationsRDTO
)
from app.adapters.dto.field_party_schedule_settings.schedule_generator_dto import ScheduleRecordDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import \
    BookingFieldPartyAndPaymentTransactionRepository
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.adapters.repository.field_party.field_party_repository import FieldPartyRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity, FieldPartyEntity, PaymentTransactionEntity, \
    BookingFieldPartyAndPaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class ReCreateClientBookingFieldRequestByIdCase(BaseUseCase[CreateBookingFieldPartyResponseDTO]):
    """
    Use Case для пересоздания платежной транзакции для существующей заявки на бронирование.

    Процесс включает:
    1. Получение существующей заявки на бронирование по ID
    2. Проверку прав доступа (заявка принадлежит текущему пользователю)
    3. Деактивацию всех предыдущих платежных транзакций
    4. Создание новой платежной транзакции через платежную систему Alatau
    5. Связывание заявки с новой транзакцией

    Используется когда:
    - Предыдущий платеж не был завершен
    - Истек срок оплаты
    - Клиент хочет повторить попытку оплаты

    Attributes:
        booking_field_party_request_repository: Репозиторий для работы с заявками на бронирование
        field_party_repository: Репозиторий для работы с партиями полей
        payment_transaction_repository: Репозиторий для работы с платежными транзакциями
        booking_field_party_and_payment_transaction_repository: Репозиторий для связей между заявками и транзакциями
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.booking_field_party_request_repository = BookingFieldPartyRequestRepository(db)
        self.field_party_repository = FieldPartyRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.booking_field_party_and_payment_transaction_repository = BookingFieldPartyAndPaymentTransactionRepository(
            db)

        self.booking_field_entity: BookingFieldPartyRequestEntity | None = None
        self.field_party: FieldPartyEntity | None = None
        self.id:int|None = None
        self.dto:CreateBookingFieldPartyRequestDTO|None = None
        self.current_user:UserWithRelationsRDTO|None = None
        self.start_at:datetime|None = None
        self.end_at:datetime|None = None
        self.response:CreateBookingFieldPartyResponseDTO = CreateBookingFieldPartyResponseDTO()
        self.unique_order = "00000000000000000000"


    async def execute(self, id: int, user: UserWithRelationsRDTO) -> CreateBookingFieldPartyResponseDTO:
        """
        Выполняет пересоздание платежной транзакции для существующей заявки на бронирование.

        Args:
            id: ID существующей заявки на бронирование
            user: Текущий пользователь (должен быть владельцем заявки)

        Returns:
            CreateBookingFieldPartyResponseDTO: Ответ с существующей заявкой и новой платежной транзакцией

        Raises:
            AppExceptionResponse.bad_request: Если срок бронирования истек
            AppExceptionResponse.not_found: Если заявка не найдена или не принадлежит пользователю
        """
        self.id = id
        self.current_user = user
        await self.validate()
        await self.transform()

        return self.response


    async def validate(self) -> None:
        """
        Валидирует данные для пересоздания платежной транзакции.

        Проверяет:
        - Наличие обязательных данных (id, user)
        - Существование заявки на бронирование
        - Заявка принадлежит текущему пользователю
        - Заявка активна (is_active = True)
        - Временной слот еще не истек (start_at >= now)
        - Существование и активность партии поля

        Raises:
            AppExceptionResponse.bad_request: Если срок бронирования истек или данные невалидны
            AppExceptionResponse.not_found: Если заявка не найдена или не принадлежит пользователю
        """
        if self.id == None or self.current_user == None:
            raise AppExceptionResponse.bad_request(i18n.gettext('data_is_not_ready'))

        self.booking_field_entity = await self.booking_field_party_request_repository.get_first_with_filters(
            filters=[
                self.booking_field_party_request_repository.model.id == self.id,
                self.booking_field_party_request_repository.model.is_active == True,
                self.booking_field_party_request_repository.model.user_id == self.current_user.id,
            ],
            options=self.booking_field_party_request_repository.default_relationships()
        )
        if not self.booking_field_entity:
            raise AppExceptionResponse.not_found(i18n.gettext('booking_field_party_request_not_found'))

        # Создаем DTO из существующей заявки
        self.dto = CreateBookingFieldPartyRequestDTO(
            field_party_id=self.booking_field_entity.field_party_id,
            day=self.booking_field_entity.start_at.strftime("%Y-%m-%d"),
            start_at=self.booking_field_entity.start_at.strftime("%H:%M"),
            end_at=self.booking_field_entity.end_at.strftime("%H:%M"),
            email=self.booking_field_entity.email,
            phone=self.booking_field_entity.phone
        )

        self.response.field_booking_request = BookingFieldPartyRequestWithRelationsRDTO.from_orm(self.booking_field_entity)

        if self.booking_field_entity.start_at > self.booking_field_entity.end_at or self.booking_field_entity.start_at < datetime.now() or self.booking_field_entity.end_at < datetime.now():
            raise AppExceptionResponse.bad_request(i18n.gettext('data_is_passed'))

        self.field_party = await self.field_party_repository.get(
            self.booking_field_entity.field_party_id,
            options=self.field_party_repository.default_relationships()
        )
        if not self.field_party:
            raise AppExceptionResponse.not_found(i18n.gettext('field_party_not_found'))
        if self.field_party.is_active is False:
            raise AppExceptionResponse.bad_request(i18n.gettext('field_party_is_not_active'))


    async def transform(self) -> None:
        """
        Трансформирует данные и создает новую платежную транзакцию.

        Выполняет следующие шаги:
        1. Деактивирует все предыдущие платежные транзакции
        2. Генерирует уникальный номер заказа и nonce
        3. Создает DTO для платежной системы Alatau с цифровой подписью
        4. Создает новую запись платежной транзакции в базе данных
        5. Связывает заявку с новой транзакцией

        В случае ошибки возвращает ответ с флагом is_success=False и сообщением об ошибке.
        """
        # 1. Деактивируем старые платежки
        # Деактивируем все платежки которые были инициированы ранее

        old_payment_transactions = await self.booking_field_party_and_payment_transaction_repository.get_with_filters(
            filters=[
                self.booking_field_party_and_payment_transaction_repository.model.request_id == self.booking_field_entity.id
            ],
            options=self.booking_field_party_and_payment_transaction_repository.default_relationships()
        )
        # Находим и деактивируем платежки
        if old_payment_transactions:
            for payment_transaction_link in old_payment_transactions:
                if payment_transaction_link.payment_transaction:
                    # Деактивируем саму платежную транзакцию
                    transaction = payment_transaction_link.payment_transaction
                    transaction.is_active = False
                    transaction.is_canceled = True
                    transaction.is_paid = False
                    payment_transaction_dto = PaymentTransactionCDTO.model_validate(transaction)
                    await self.payment_transaction_repository.update(obj=transaction, dto=payment_transaction_dto)

            # Деактивируем связи между заказом и транзакциями
            await self.booking_field_party_and_payment_transaction_repository.deactivate_links_for_request(
                request_id=self.booking_field_entity.id
            )
        # 2. Создадим платежную транзакцию
        try:
            # Генерируем уникальный номер заказа для платежной системы
            self.unique_order = await self.payment_transaction_repository.generate_unique_order(min_len=6, max_len=22)
            nonce = await self.payment_transaction_repository.generate_unique_noncense()
            user_name = f"{self.current_user.first_name or ''} {self.current_user.last_name or ''}".strip()

            # Создаем DTO для платежной системы Alatau
            desc_text = f"Бронирование {self.field_party.title_ru} {self.dto.start_at}"[:50]
            self.order_dto = AlatauCreateResponseOrderDTO(
                ORDER=self.unique_order,
                AMOUNT=self.booking_field_entity.total_price,
                DESC=desc_text,
                EMAIL=self.booking_field_entity.email,
                NONCE=nonce,
                CLIENT_ID=self.current_user.id,
                NAME=user_name,
                BACKREF=app_config.booking_field_backref
            )

            # Формируем цифровую подпись для безопасности
            self.order_dto.set_signature(app_config.shared_secret)

            # Создаем DTO для платежной транзакции
            payment_cdto = PaymentTransactionCDTO(
                user_id=self.current_user.id,
                status_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                transaction_type=DbValueConstants.PaymentBookingFieldType,
                order=self.unique_order,
                nonce=self.order_dto.NONCE,
                amount=self.booking_field_entity.total_price,
                currency="KZT",
                merchant=app_config.merchant_id,
                language="ru",
                client_id=self.current_user.id,
                desc=desc_text,
                wtype=self.order_dto.WTYPE,
                backref=self.order_dto.BACKREF,
                email=self.booking_field_entity.email,
                name=self.order_dto.NAME if hasattr(self.order_dto, 'NAME') else None,
                pre_p_sign=self.order_dto.P_SIGN,
                is_active=True,
                is_paid=False,
                is_canceled=False,
                expired_at=self.booking_field_entity.paid_until
            )

            # Создаем запись платежной транзакции в базе данных
            self.payment_transaction_entity = await self.payment_transaction_repository.create(
                PaymentTransactionEntity(**payment_cdto.model_dump())
            )

            # 5. Создаем связь между заказом и платежной транзакцией
            await self.booking_field_party_and_payment_transaction_repository.create(
                BookingFieldPartyAndPaymentTransactionEntity(
                    request_id=self.booking_field_entity.id,
                    payment_transaction_id=self.payment_transaction_entity.id,
                    link_type="initial",  # Тип связи: первоначальная транзакция
                    link_reason="Initial order creation",
                    is_primary=True,  # Основная транзакция для заказа
                    is_active=True
                )
            )

            # Заполняем успешный ответ
            self.response.order = self.order_dto
            self.response.payment_transaction = PaymentTransactionRDTO.model_validate(self.payment_transaction_entity)
            self.response.is_success = True

        except Exception as e:
            # Мягкая обработка ошибок платежной системы (не прерываем процесс)
            self.response.is_success = False
            self.response.message = traceback.format_exc()








