from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketWithRelationsRDTO,
    YandexAfishaWidgetTicketCDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import (
    PaginationYandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.filters.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_filter import (
    YandexAfishaWidgetTicketFilter,
)
from app.adapters.filters.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_pagination_filter import (
    YandexAfishaWidgetTicketPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.yandex_afisha_widget_ticket.all_yandex_afisha_widget_ticket_case import (
    AllYandexAfishaWidgetTicketCase,
)
from app.use_case.yandex_afisha_widget_ticket.create_yandex_afisha_widget_ticket_case import (
    CreateYandexAfishaWidgetTicketCase,
)
from app.use_case.yandex_afisha_widget_ticket.delete_yandex_afisha_widget_ticket_case import (
    DeleteYandexAfishaWidgetTicketCase,
)
from app.use_case.yandex_afisha_widget_ticket.get_yandex_afisha_widget_ticket_by_id_case import (
    GetYandexAfishaWidgetTicketByIdCase,
)
from app.use_case.yandex_afisha_widget_ticket.paginate_yandex_afisha_widget_ticket_case import (
    PaginateYandexAfishaWidgetTicketCase,
)
from app.use_case.yandex_afisha_widget_ticket.update_yandex_afisha_widget_ticket_case import (
    UpdateYandexAfishaWidgetTicketCase,
)
from app.use_case.yandex_afisha_widget_ticket.upload_image_yandex_afisha_widget_ticket_case import (
    UploadImageYandexAfishaWidgetTicketCase,
)


class YandexAfishaWidgetTicketApi:
    def __init__(self) -> None:
        """
        Инициализация YandexAfishaWidgetTicketApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API билетов Яндекс.Афиша.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationYandexAfishaWidgetTicketWithRelationsRDTO,
            summary="Список билетов Яндекс.Афиша с пагинацией",
            description="Получение списка билетов Яндекс.Афиша с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[YandexAfishaWidgetTicketWithRelationsRDTO],
            summary="Список всех билетов Яндекс.Афиша",
            description="Получение полного списка билетов Яндекс.Афиша",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=YandexAfishaWidgetTicketWithRelationsRDTO,
            summary="Создать билет Яндекс.Афиша",
            description="Создание нового билета Яндекс.Афиша",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=YandexAfishaWidgetTicketWithRelationsRDTO,
            summary="Обновить билет Яндекс.Афиша по ID",
            description="Обновление информации о билете Яндекс.Афиша по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=YandexAfishaWidgetTicketWithRelationsRDTO,
            summary="Получить билет Яндекс.Афиша по ID",
            description="Получение информации о билете Яндекс.Афиша по ID",
        )(self.get_by_id)

        self.router.put(
            "/upload-image/{id}",
            response_model=YandexAfishaWidgetTicketWithRelationsRDTO,
            summary="Загрузить/обновить изображение билета Яндекс.Афиша",
            description="Загрузка или обновление изображения билета Яндекс.Афиша по его ID",
        )(self.upload_image)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить билет Яндекс.Афиша по ID",
            description="Удаление билета Яндекс.Афиша по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: YandexAfishaWidgetTicketPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationYandexAfishaWidgetTicketWithRelationsRDTO:
        try:
            return await PaginateYandexAfishaWidgetTicketCase(db).execute(filter)
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
        filter: YandexAfishaWidgetTicketFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[YandexAfishaWidgetTicketWithRelationsRDTO]:
        try:
            return await AllYandexAfishaWidgetTicketCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: YandexAfishaWidgetTicketCDTO = Depends(
            FormParserHelper.parse_yandex_afisha_widget_ticket_dto_from_form
        ),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        try:
            return await CreateYandexAfishaWidgetTicketCase(db).execute(
                dto=dto, file=file
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: YandexAfishaWidgetTicketCDTO = Depends(
            FormParserHelper.parse_yandex_afisha_widget_ticket_dto_from_form
        ),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        try:
            return await UpdateYandexAfishaWidgetTicketCase(db).execute(
                id=id, dto=dto, file=file
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        try:
            return await GetYandexAfishaWidgetTicketByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        try:
            return await DeleteYandexAfishaWidgetTicketCase(db).execute(
                id=id, force_delete=force_delete
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def upload_image(
        self,
        id: RoutePathConstants.IDPath,
        file: UploadFile = File(..., description="Файл изображения билета Яндекс.Афиша"),
        db: AsyncSession = Depends(get_db),
    ) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        try:
            return await UploadImageYandexAfishaWidgetTicketCase(db).execute(
                id=id, file=file
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc