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
from app.use_case.field_party_schedule.preview_field_party_schedule_case import PreviewFieldPartyScheduleCase


class CreateClientBookingFieldRequestCase(BaseUseCase[CreateBookingFieldPartyResponseDTO]):
    """
    Use Case для создания клиентской заявки на бронирование поля.

    Процесс включает:
    1. Валидацию данных бронирования и проверку доступности временного слота
    2. Создание заявки на бронирование со статусом "Ожидание оплаты"
    3. Создание платежной транзакции через платежную систему Alatau
    4. Связывание заявки с платежной транзакцией

    Attributes:
        booking_field_party_request_repository: Репозиторий для работы с заявками на бронирование
        field_party_repository: Репозиторий для работы с партиями полей
        payment_transaction_repository: Репозиторий для работы с платежными транзакциями
        booking_field_party_and_payment_transaction_repository: Репозиторий для связей между заявками и транзакциями
        preview_field_party_schedule_case: Use Case для получения расписания поля
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
        self.preview_field_party_schedule_case = PreviewFieldPartyScheduleCase(db)

        self.booking_field_entity: BookingFieldPartyRequestEntity | None = None
        self.field_party: FieldPartyEntity | None = None
        self.dto:CreateBookingFieldPartyRequestDTO|None = None
        self.current_user:UserWithRelationsRDTO|None = None
        self.start_at:datetime|None = None
        self.end_at:datetime|None = None
        self.active_schedule:ScheduleRecordDTO|None = None
        self.response:CreateBookingFieldPartyResponseDTO = CreateBookingFieldPartyResponseDTO()
        self.unique_order = "00000000000000000000"


    async def execute(self, dto: CreateBookingFieldPartyRequestDTO, user: UserWithRelationsRDTO) -> CreateBookingFieldPartyResponseDTO:
        """
        Выполняет создание заявки на бронирование поля и инициализацию платежной транзакции.

        Args:
            dto: DTO с данными для создания заявки (field_party_id, день, время начала/окончания, контакты)
            user: Текущий пользователь, создающий заявку

        Returns:
            CreateBookingFieldPartyResponseDTO: Ответ с созданной заявкой, платежной транзакцией и данными для оплаты

        Raises:
            AppExceptionResponse.bad_request: Если данные невалидны или временной слот недоступен
            AppExceptionResponse.not_found: Если партия поля не найдена
        """
        self.dto = dto
        self.current_user = user
        await self.validate()
        await self.transform()

        return self.response


    async def validate(self) -> None:
        """
        Валидирует входные данные и проверяет доступность временного слота.

        Проверяет:
        - Наличие обязательных данных (dto, user)
        - Корректность формата даты и времени
        - Временной слот находится в будущем
        - Существование и активность партии поля
        - Доступность временного слота в расписании
        - Слот не забронирован другим пользователем

        Raises:
            AppExceptionResponse.bad_request: При невалидных данных или недоступном слоте
            AppExceptionResponse.not_found: Если партия поля не найдена
        """
        if self.dto == None or self.current_user == None:
            raise AppExceptionResponse.bad_request(i18n.gettext('data_is_not_ready'))
        try:
            self.start_at = datetime.strptime(f"{self.dto.day} {self.dto.start_at}", "%Y-%m-%d %H:%M")
            self.end_at = datetime.strptime(f"{self.dto.day} {self.dto.end_at}", "%Y-%m-%d %H:%M")
        except Exception as exc:
            raise AppExceptionResponse.bad_request(i18n.gettext('data_not_is_right'))

        if self.start_at > self.end_at or self.start_at < datetime.now() or self.end_at < datetime.now():
            raise AppExceptionResponse.bad_request(i18n.gettext('data_is_passed'))

        self.field_party = await self.field_party_repository.get(
            self.dto.field_party_id,
            options=self.field_party_repository.default_relationships()
        )
        if not self.field_party:
            raise AppExceptionResponse.bad_request(i18n.gettext('field_party_not_found'))
        if self.field_party.is_active is False:
            raise AppExceptionResponse.bad_request(i18n.gettext('field_party_is_not_active'))

        try:
            schedule_response = await self.preview_field_party_schedule_case.execute(self.dto.field_party_id, self.dto.day)
            if schedule_response.schedule_records == None or len(schedule_response.schedule_records) == 0:
                raise AppExceptionResponse.bad_request(i18n.gettext('field_party_schedule_is_not_active'))
            for record in schedule_response.schedule_records:
                if record.start_at == self.dto.start_at and record.end_at == self.dto.end_at:
                    self.active_schedule = record
                    break
        except Exception as exc:
            raise AppExceptionResponse.bad_request(i18n.gettext('there_is_no_schedule'))

        if self.active_schedule == None:
            raise AppExceptionResponse.bad_request(i18n.gettext('there_is_no_schedule'))


    async def transform(self) -> None:
        """
        Трансформирует и сохраняет данные заявки и платежной транзакции.

        Выполняет следующие шаги:
        1. Создает заявку на бронирование со статусом "Ожидание оплаты"
        2. Генерирует уникальный номер заказа и nonce для платежной системы
        3. Формирует DTO для платежной системы Alatau с цифровой подписью
        4. Создает запись платежной транзакции в базе данных
        5. Связывает заявку с платежной транзакцией

        В случае ошибки на этапе платежа, заявка остается в системе, но ответ содержит флаг is_success=False
        """
        # 1. Создадим заявку на бронирование
        try:
            dto = BookingFieldPartyRequestCDTO(
                    status_id=DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentID,
                    field_id=self.field_party.field_id,
                    field_party_id=self.field_party.id,
                    user_id=self.current_user.id,
                    email=self.dto.email if self.dto.email else self.current_user.email,
                    phone=self.dto.phone if self.dto.phone else self.current_user.phone,
                    total_price=self.active_schedule.price,
                    start_at=self.start_at,
                    end_at=self.end_at,
                    paid_until=datetime.now() + timedelta(hours=1)
                )
            self.booking_field_entity = await self.booking_field_party_request_repository.create(
                self.booking_field_party_request_repository.model(**dto.dict())
            )
            self.booking_field_entity = await self.booking_field_party_request_repository.get(
                self.booking_field_entity.id,
                options=self.booking_field_party_request_repository.default_relationships()
            )

            self.response.field_booking_request = BookingFieldPartyRequestWithRelationsRDTO.from_orm(self.booking_field_entity)
        except Exception as exc:

            raise AppExceptionResponse.bad_request(i18n.gettext('booking_field_not_created' + traceback.format_exc()))

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
                AMOUNT=self.active_schedule.price,
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
                amount=self.active_schedule.price,
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







