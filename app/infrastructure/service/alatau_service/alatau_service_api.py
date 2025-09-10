from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingRequestDTO, TicketonBookingShowBookingDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
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