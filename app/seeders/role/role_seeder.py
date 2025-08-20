from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import RoleEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class RoleSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        roles = self.get_data()
        await self.load_seeders(RoleEntity, session, AppTableNames.RoleTableName, roles)

    def get_dev_data(self) -> list[RoleEntity]:
        return [
            RoleEntity(
                id=DbValueConstants.AdminRoleConstantID,
                title_ru="Администратор системы",
                title_kk="Жүйе әкімшісі",
                title_en="System Administrator",
                description_ru="Управление учетными записями пользователей, настройка прав доступа, контроль работы системы",
                description_kk="Пайдаланушылардың есептік жазбаларын басқару, қолжетімділікті орнату, жүйенің жұмысын бақылау",
                description_en="User account management, access rights configuration, system monitoring",
                value=DbValueConstants.AdminRoleConstantValue,
                is_active=True,
                can_register=False,
                is_system=True,
                is_administrative=True,
            ),
            RoleEntity(
                id=DbValueConstants.ClientRoleConstantID,
                title_ru="Клиент",
                title_kk="Клиент",
                title_en="Client",
                description_ru="Пользователь системы с базовыми возможностями для работы с сервисами",
                description_kk="Қызметтермен жұмыс істеуге арналған негізгі мүмкіндіктері бар жүйе пайдаланушысы",
                description_en="System user with basic access to services",
                value=DbValueConstants.ClientRoleConstantValue,
                is_active=True,
                can_register=True,
                is_system=True,
                is_administrative=False,
            ),
        ]

    def get_prod_data(self) -> list[RoleEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
