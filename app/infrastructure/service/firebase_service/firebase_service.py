import traceback
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.firebase_notification.firebase_notification_repository import \
    FirebaseNotificationRepository
from app.entities import NotificationEntity


async def initialize_firebase() -> None:
    # BASE_DIR указывает на корень проекта (где .env и firebase-admin.json)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent  # поднимаемся выше
    cred_path = BASE_DIR / "firebase-admin.json"

    if not cred_path.exists():
        raise FileNotFoundError(f"Firebase key not found: {cred_path}")

    cred = credentials.Certificate(str(cred_path))

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)



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
