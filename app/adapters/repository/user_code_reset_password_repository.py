from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.base_repository import BaseRepository
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity


class UserCodeResetPasswordRepository(BaseRepository[UserCodeResetPasswordEntity]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserCodeResetPasswordEntity, db)
