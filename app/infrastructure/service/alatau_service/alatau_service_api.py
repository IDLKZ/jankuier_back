import httpx

from app.adapters.dto.alatau.alatau_cancel_payment_dto import AlatauCancelPaymentDTO
from app.adapters.dto.alatau.alatau_cancel_payment_response_dto import AlatauRefundPaymentResultDTO
from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.alatau.alatau_status_request_dto import AlatauStatusRequestDTO
from app.adapters.dto.alatau.alatau_status_response_dto import AlatauPaymentStatusResponseDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingRequestDTO, TicketonBookingShowBookingDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.helpers.alatau_helper import AlatauHelper
from app.infrastructure.app_config import app_config
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI


class AlatauServiceAPI:
    shared_token:str = app_config.shared_secret
    def __init__(self, shared_token: str|None = None):
        if(shared_token):
            self.shared_token = shared_token


    async def create_for_ticketon_booking(self,dto: TicketonBookingShowBookingDTO,user:UserWithRelationsRDTO|None = None):
        show:TicketonSingleShowResponseDTO|None = await TicketonServiceAPI().get_ticketon_single_show(int(dto.show),get_from_redis=True)
        order = AlatauCreateResponseOrderDTO()
        order.ORDER = dto.sale
        order.AMOUNT = dto.sum
        order.DESC = "Покупка билетов на мероприятие"
        order.DESC_ORDER = AlatauHelper.make_desc(dto,show)
        order.EMAIL = "mistier.famous@gmail.com"
        order.set_signature(self.shared_token)
        return order


    async def payment_refund(self,dto:AlatauCancelPaymentDTO)->AlatauRefundPaymentResultDTO:
        try:
            url = app_config.alatau_payment_refund_post_url
            dto.set_signature(app_config.shared_secret)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=url,
                    data=dto.to_form_data(),
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                xml_response = response.text
                return AlatauRefundPaymentResultDTO.from_xml(xml_response)
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Alatau Refund ERROR: {str(e)}"
            ) from e

    async def get_payment_status(self,dto:AlatauStatusRequestDTO)->AlatauPaymentStatusResponseDTO:
        try:
            url = app_config.alatau_payment_status_post_url
            dto.set_signature(app_config.shared_secret)
            print(dto)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=url,
                    data=dto.to_form_data(),
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                xml_response = response.text
                return AlatauPaymentStatusResponseDTO.from_xml(xml_response)
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Alatau Refund ERROR: {str(e)}"
            ) from e