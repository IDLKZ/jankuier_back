import urllib.parse

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.ticketon_order.ticketon_order_dto import (
    TicketonOrderRDTO,
    TicketonOrderWithRelationsRDTO,
)
from app.adapters.dto.ticketon.ticketon_order_check_response_dto import TicketonOrderCheckCommonResponseDTO
from app.adapters.dto.ticketon.ticketon_ticket_check_response_dto import TicketonTicketCheckCommonResponseDTO
from app.adapters.dto.pagination_dto import PaginationTicketonOrderWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingRequestDTO
from app.adapters.dto.ticketon.ticketon_response_for_sale_dto import TicketonResponseForSaleDTO
from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefResponseDTO, AlatauBackrefPostDTO, AlatauBackrefGetDTO
from app.adapters.filters.ticketon_order.ticketon_order_filter import TicketonOrderFilter
from app.adapters.filters.ticketon_order.ticketon_order_pagination_filter import TicketonOrderPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.ticketon_order.all_ticketon_order_case import AllTicketonOrderCase
from app.use_case.ticketon_order.get_ticketon_order_by_id_case import GetTicketonOrderByIdCase
from app.use_case.ticketon_order.paginate_ticketon_order_case import PaginateTicketonOrderCase
from app.use_case.ticketon_order.client.create_sale_case import CreateSaleTicketonAndOrderCase
from app.use_case.ticketon_order.client.recreate_payment_case import RecreatePaymentForTicketonOrderCase
from app.use_case.ticketon_order.client.ticketon_confirm_sale import TicketonConfirmCase
from app.use_case.ticketon_order.client.refund_ticketon_order_case import RefundTicketonOrderCase
from app.use_case.ticketon_order.client.check_ticketon_order_case import CheckTicketonOrderCase
from app.use_case.ticketon_order.client.check_ticketon_ticket_case import CheckTicketonTicketCase


class TicketonOrderApi:
    """
    API класс для управления заказами Ticketon.
    
    Предоставляет REST API эндпоинты для операций с заказами Ticketon.
    Включает операции: получение всех, получение по ID, пагинация, создание продажи.
    
    Примечание: Данный API предоставляет операции чтения (All, Get, Paginate)
    и создания продажи билетов через Ticketon API.
    """

    def __init__(self) -> None:
        """
        Инициализация TicketonOrderApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API заказов Ticketon.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрирует все маршруты API для заказов Ticketon.
        """
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationTicketonOrderWithRelationsRDTO,
            summary="Пагинация заказов Ticketon",
            description="Получение пагинированного списка заказов Ticketon с отношениями",
        )(self.paginate)
        
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[TicketonOrderRDTO],
            summary="Список всех заказов Ticketon",
            description="Получение полного списка заказов Ticketon",
        )(self.get_all)
        
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=TicketonOrderRDTO,
            summary="Получить заказ Ticketon по ID",
            description="Получение заказа Ticketon по уникальному идентификатору",
        )(self.get)
        
        self.router.post(
            "/create-sale",
            response_model=TicketonResponseForSaleDTO,
            summary="Создать продажу билетов Ticketon",
            description="Создание заказа и транзакции оплаты для покупки билетов через Ticketon API",
        )(self.create_sale)
        
        self.router.post(
            "/recreate-payment/{ticketon_order_id}",
            response_model=TicketonResponseForSaleDTO,
            summary="Пересоздать платеж для заказа Ticketon",
            description="Находит активную транзакцию или создает новую для существующего заказа Ticketon",
        )(self.recreate_payment)
        
        self.router.get(
            "/confirm-sale-get",
            response_model=AlatauBackrefResponseDTO,
            summary="Подтверждение оплаты Ticketon (GET)",
            description="Обработка GET-запроса подтверждения оплаты от платежной системы Alatau",
        )(self.confirm_sale_get)
        
        self.router.post(
            "/confirm-sale-post",
            response_model=AlatauBackrefResponseDTO,
            summary="Подтверждение оплаты Ticketon (POST)",
            description="Обработка POST-запроса подтверждения оплаты от платежной системы Alatau",
        )(self.confirm_sale_post)
        
        self.router.post(
            "/refund-sale/{sale}",
            response_model=TicketonResponseForSaleDTO,
            summary="Возврат билетов Ticketon",
            description="Отмена заказа в Ticketon и возврат денежных средств через банк Алатау",
        )(self.refund_sale)

        self.router.get(
            "/check-order/{ticketon_order_id}",
            response_model=TicketonOrderCheckCommonResponseDTO,
            summary="Проверка заказа Ticketon",
            description="Получение актуальной информации о заказе из API Ticketon",
        )(self.check_order)

        self.router.get(
            "/check-ticket/{ticketon_order_id}/{ticket_id}",
            response_model=TicketonTicketCheckCommonResponseDTO,
            summary="Проверка билета Ticketon",
            description="Получение актуальной информации о конкретном билете из API Ticketon",
        )(self.check_ticket)

    async def paginate(
        self,
        filter: TicketonOrderPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationTicketonOrderWithRelationsRDTO:
        """
        Получение пагинированного списка заказов Ticketon с отношениями.
        
        Args:
            filter: Фильтр для пагинации с параметрами сортировки и поиска
            db: Сессия базы данных
            
        Returns:
            Пагинированный список заказов с отношениями
        """
        try:
            return await PaginateTicketonOrderCase(db).execute(filter=filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: TicketonOrderFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[TicketonOrderRDTO]:
        """
        Получение полного списка заказов Ticketon.
        
        Args:
            filter: Фильтр для поиска и сортировки
            db: Сессия базы данных
            
        Returns:
            Список всех заказов Ticketon
        """
        try:
            return await AllTicketonOrderCase(db).execute(filter=filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonOrderRDTO:
        """
        Получение заказа Ticketon по ID.
        
        Args:
            id: Уникальный идентификатор заказа
            db: Сессия базы данных
            
        Returns:
            Найденный заказ Ticketon
        """
        try:
            return await GetTicketonOrderByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create_sale(
        self,
        dto: TicketonBookingRequestDTO,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonResponseForSaleDTO:
        """
        Создание продажи билетов через Ticketon API.
        
        Создаёт заказ в системе Ticketon, формирует транзакцию оплаты в Alatau
        и связывает их между собой. Без авторизации пользователя.
        
        Args:
            dto: Данные для создания заказа (показ, билеты, контактная информация)
            db: Сессия базы данных
            
        Returns:
            Ответ с данными заказа Ticketon, транзакции оплаты и ID платежа
        """
        try:
            return await CreateSaleTicketonAndOrderCase(db).execute(dto=dto, user=None)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def recreate_payment(
        self,
        ticketon_order_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonResponseForSaleDTO:
        """
        Пересоздание/восстановление платежа для существующего заказа Ticketon.
        
        Находит активную payment_transaction для заказа или создает новую.
        Логика:
        1. Проверяет существование и валидность заказа Ticketon
        2. Ищет активную payment_transaction (is_active=True, is_paid=False, is_canceled=False, не истекшая)
        3. Если активная найдена - возвращает её данные
        4. Если не найдена - создает новую payment_transaction
        5. Деактивирует старые транзакции
        
        Args:
            ticketon_order_id: ID заказа Ticketon
            db: Сессия базы данных
            
        Returns:
            TicketonResponseForSaleDTO с данными для оплаты
        """
        try:
            return await RecreatePaymentForTicketonOrderCase(db).execute(
                ticketon_order_id=ticketon_order_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def confirm_sale_get(
        self,
        order: str = Query(..., description="Номер заказа"),
        mpi_order: str = Query(..., description="Номер заказа в MPI"),
        amount: str = Query(..., description="Сумма платежа"),
        currency: str = Query(..., description="Валюта платежа"),
        res_code: str = Query(..., description="Код результата"),
        res_desc: str = Query(None, description="Описание результата"),
        rrn: str = Query(None, description="RRN (возвращается в REF, тольков случаеуспешной операции)"),
        sign: str = Query(..., description="Электронная подпись"),
        db: AsyncSession = Depends(get_db),
    ) -> AlatauBackrefResponseDTO:
        """
        Обработка GET-запроса подтверждения оплаты от платежной системы Alatau.
        
        Обрабатывает результат оплаты, полученный через GET-параметры от платежной системы.
        Подтверждает заказ в Ticketon при успешной оплате.
        
        Args:
            order: Номер заказа в платежной системе
            mpi_order: Номер заказа в MPI
            amount: Сумма платежа
            currency: Валюта платежа (обычно KZT)
            res_code: Код результата ("0" - успех, другие - ошибка)
            res_desc: Описание результата (опционально)
            rrn: Дополнительное описание (опционально)
            sign: Электронная подпись для верификации
            db: Сессия базы данных
            
        Returns:
            Результат обработки платежа с информацией о заказе и транзакции
        """
        try:
            decoded_res_desc = urllib.parse.unquote_plus(res_desc or "")
            dto = AlatauBackrefGetDTO(
                order=order,
                mpi_order=mpi_order,
                amount=amount,
                currency=currency,
                res_code=res_code,
                res_desc=decoded_res_desc,
                rrn=rrn,
                sign=sign
            )
            return await TicketonConfirmCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def confirm_sale_post(
        self,
        dto: AlatauBackrefPostDTO,
        db: AsyncSession = Depends(get_db),
    ) -> AlatauBackrefResponseDTO:
        """
        Обработка POST-запроса подтверждения оплаты от платежной системы Alatau.
        
        Обрабатывает результат оплаты, полученный через POST-данные от платежной системы.
        Подтверждает заказ в Ticketon при успешной оплате.
        
        Args:
            dto: Данные платежа от системы Alatau
            db: Сессия базы данных
            
        Returns:
            Результат обработки платежа с информацией о заказе и транзакции
        """
        try:
            return await TicketonConfirmCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def refund_sale(
        self,
        sale: str,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonResponseForSaleDTO:
        """
        Возврат билетов и денежных средств для заказа Ticketon.
        
        Выполняет полный цикл возврата:
        1. Проверяет статус заказа и возможность возврата
        2. Отменяет бронирование в системе Ticketon (если еще не отменено)
        3. Инициирует возврат денежных средств через банк Алатау
        4. Обновляет статусы заказа и платежной транзакции
        
        Поддерживаемые статусы заказа для возврата:
        - PaidConfirmed: Заказ оплачен и подтвержден (выполняется отмена в Ticketon + возврат средств)
        - CancelledAwaitingRefund: Заказ отменен, ожидает возврата средств (только возврат средств)
        
        Args:
            sale: Номер продажи (sale) в системе Ticketon
            db: Сессия базы данных
            
        Returns:
            TicketonResponseForSaleDTO: Результат операции возврата с обновленными данными
            
        Raises:
            AppExceptionResponse: При ошибках валидации или внешних API
        """
        try:
            return await RefundTicketonOrderCase(db).execute(sale=sale, user=None)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def check_order(
        self,
        ticketon_order_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonOrderCheckCommonResponseDTO:
        """
        Проверка заказа Ticketon через API.

        Получает актуальную информацию о заказе из системы Ticketon
        и объединяет её с локальными данными заказа.

        Args:
            ticketon_order_id: ID заказа для проверки
            db: Сессия базы данных

        Returns:
            TicketonOrderCheckCommonResponseDTO: Объединенные данные заказа и проверки

        Raises:
            HTTPException: При ошибке валидации или получения данных
        """
        try:
            return await CheckTicketonOrderCase(db).execute(
                ticketon_order_id=ticketon_order_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def check_ticket(
        self,
        ticketon_order_id: RoutePathConstants.IDPath,
        ticket_id: str,
        db: AsyncSession = Depends(get_db),
    ) -> TicketonTicketCheckCommonResponseDTO:
        """
        Проверка конкретного билета Ticketon через API.

        Получает актуальную информацию о билете из системы Ticketon
        и объединяет её с локальными данными заказа.

        Args:
            ticketon_order_id: ID заказа, содержащего билет
            ticket_id: ID билета для проверки
            db: Сессия базы данных

        Returns:
            TicketonTicketCheckCommonResponseDTO: Объединенные данные заказа и проверки билета

        Raises:
            HTTPException: При ошибке валидации или получения данных
        """
        try:
            return await CheckTicketonTicketCase(db).execute(
                ticketon_order_id=ticketon_order_id,
                ticketon_ticket_id=ticket_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc