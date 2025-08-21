from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth_core import get_password_hash
from app.entities import UserEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class UserSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        roles = self.get_data()
        await self.load_seeders(UserEntity, session, AppTableNames.UserTableName, roles)

    def get_dev_data(self) -> list[UserEntity]:
        return [
            UserEntity(
                id=1,
                role_id=DbValueConstants.AdminRoleConstantID,
                image_id=None,
                region_id=None,
                email="admin@example.com",
                phone="+77000000001",
                sex=1,
                username="admin",
                iin="123456789012",
                birthdate=date(2000, 8, 1),
                first_name="Админ",
                last_name="Системы",
                patronomic=None,
                password_hash=get_password_hash("admin123"),
                is_active=True,
                is_verified=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            UserEntity(
                id=2,
                role_id=DbValueConstants.ClientRoleConstantID,
                image_id=None,
                region_id=None,
                email="client@example.com",
                phone="+77000000002",
                sex=1,
                username="client",
                iin="987654321098",
                birthdate=date(2001, 1, 15),
                first_name="Иван",
                last_name="Иванов",
                patronomic="Иванович",
                password_hash=get_password_hash("client123"),
                is_active=True,
                is_verified=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
        ]

    def get_prod_data(self) -> list[UserEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
