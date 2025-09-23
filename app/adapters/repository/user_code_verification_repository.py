from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.base_repository import BaseRepository
from app.entities.user_code_verification_entity import UserCodeVerificationEntity


class UserCodeVerificationRepository(BaseRepository[UserCodeVerificationEntity]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserCodeVerificationEntity, db)