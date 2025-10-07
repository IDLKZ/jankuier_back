import traceback
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.firebase_notification.firebase_notification_repository import \
    FirebaseNotificationRepository
from app.adapters.repository.notification.notification_repository import NotificationRepository
from app.entities import NotificationEntity, ProductOrderEntity, TicketonOrderEntity, BookingFieldPartyRequestEntity
from app.shared.db_value_constants import DbValueConstants


async def initialize_firebase() -> None:
    # BASE_DIR указывает на корень проекта (где .env и firebase-admin.json)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent  # поднимаемся выше
    cred_path = BASE_DIR / "firebase-admin.json"

    if not cred_path.exists():
        raise FileNotFoundError(f"Firebase key not found: {cred_path}")

    cred = credentials.Certificate(str(cred_path))

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred,{
            "projectId": "kz-kff-jankuier-mobile"
        })



class FireBaseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def send_notifications_async(self,notification: NotificationEntity):
        firebaseNotificationRepository: FirebaseNotificationRepository = FirebaseNotificationRepository(db=self.db)
        try:
            if notification.user_id != None:
                device = await firebaseNotificationRepository.get_first_with_filters(
                    filters=[
                        firebaseNotificationRepository.model.user_id == notification.user_id,
                        firebaseNotificationRepository.model.is_active.is_(True)
                    ]
                )
                if device:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=notification.title_ru,
                            body=notification.description_ru,
                        ),
                        token=device.token,
                    )
                    response = messaging.send(message)

            if notification.user_id == None and notification.topics != None:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification.title_ru,
                        body=notification.description_ru,
                    ),
                    topic="all_users",  # все подписанные на тему "all_users"
                )
                response = messaging.send(message)
        except Exception as e:
            traceback.print_exc()


    async def send_payment_product_successfull_notification(self,user_id: int, productOrder:ProductOrderEntity):
        try:
            notification_repository = NotificationRepository(self.db)
            notification_model = NotificationEntity(
                topic_id=DbValueConstants.TopicNotificationShopID,
                user_id=user_id,
                is_active=True,
                title_ru=f"Оплата заказа № {productOrder.id} на сумму {productOrder.total_price} прошла успешно",
                title_kk=f"Тапсырыс № {productOrder.id} {productOrder.total_price} сомасына сәтті төленді",
                title_en=f"Payment for order № {productOrder.id} in the amount of {productOrder.total_price} was successful",
                description_ru=f"Оплата товаров на сумму {productOrder.total_price} прошла успешно, уникальный номер заказа - {productOrder.paid_order}",
                description_kk=f"{productOrder.total_price} сомасына төлем сәтті өтті, тапсырыстың бірегей нөмірі — {productOrder.paid_order}",
                description_en=f"Payment of goods in the amount of {productOrder.total_price} was successful, your unique order number is {productOrder.paid_order}",
            )
            notification = await notification_repository.create(notification_model)
            await self.send_notifications_async(notification)
        except Exception as exc:
            exc.with_traceback()


    async def send_ticketon_notification(self,user_id: int, ticketon:TicketonOrderEntity):
        try:
            notification_repository = NotificationRepository(self.db)
            notification_model = NotificationEntity(
                topic_id=DbValueConstants.TopicNotificationShopID,
                user_id=user_id,
                is_active=True,
                title_ru=f"Оплата билета № {ticketon.sale} на сумму {ticketon.price} прошла успешно",
                title_kk=f"Билет № {ticketon.sale} {ticketon.price} сомасына сәтті төленді",
                title_en=f"Payment for ticket № {ticketon.sale} in the amount of {ticketon.price} was successful",
                description_ru=f"Оплата билетов на сумму {ticketon.price} прошла успешно, уникальный номер заказа - {ticketon.sale}",
                description_kk=f"{ticketon.price} сомасына төлем сәтті өтті, тапсырыстың бірегей нөмірі — {ticketon.sale}",
                description_en=f"Payment of tickets in the amount of {ticketon.price} was successful, your unique order number is {ticketon.sale}",
            )
            notification = await notification_repository.create(notification_model)
            await self.send_notifications_async(notification)
        except Exception as exc:
            exc.with_traceback()

    async def send_booking_field_notification(
            self,
            user_id: int,
            bookingFieldRequest: BookingFieldPartyRequestEntity
    ):
        try:
            notification_repository = NotificationRepository(self.db)

            notification_model = NotificationEntity(
                topic_id=DbValueConstants.TopicNotificationShopID,
                user_id=user_id,
                is_active=True,

                # Заголовки
                title_ru=f"Оплата брони № {bookingFieldRequest.id} на сумму {bookingFieldRequest.total_price} прошла успешно",
                title_kk=f"Бронь № {bookingFieldRequest.id} {bookingFieldRequest.total_price} сомасына сәтті төленді",
                title_en=f"Payment for booking № {bookingFieldRequest.id} in the amount of {bookingFieldRequest.total_price} was successful",

                # Описания
                description_ru=f"Оплата брони на сумму {bookingFieldRequest.total_price} прошла успешно, уникальный номер заказа - {bookingFieldRequest.paid_order}",
                description_kk=f"{bookingFieldRequest.total_price} сомасына төлем сәтті өтті, тапсырыстың бірегей нөмірі — {bookingFieldRequest.paid_order}",
                description_en=f"Payment of booking in the amount of {bookingFieldRequest.total_price} was successful, your unique order number is {bookingFieldRequest.paid_order}",
            )

            notification = await notification_repository.create(notification_model)
            await self.send_notifications_async(notification)

        except Exception as exc:
            exc.with_traceback()




