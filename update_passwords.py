"""
Скрипт для обновления паролей пользователей admin и client в базе данных
после изменения требований к валидации паролей.
"""
import asyncio
from sqlalchemy import select, update
from app.infrastructure.db import AsyncSessionLocal
from app.entities import UserEntity
from app.core.auth_core import get_password_hash


async def update_user_passwords():
    """Обновляет пароли для пользователей admin и client"""
    async with AsyncSessionLocal() as session:
        try:
            # Обновляем пароль для admin
            stmt_admin = (
                update(UserEntity)
                .where(UserEntity.username == "admin")
                .values(password_hash=get_password_hash("Admin123!"))
            )
            result_admin = await session.execute(stmt_admin)

            # Обновляем пароль для client
            stmt_client = (
                update(UserEntity)
                .where(UserEntity.username == "client")
                .values(password_hash=get_password_hash("Client123!"))
            )
            result_client = await session.execute(stmt_client)

            await session.commit()

            print(f"[OK] Пароль для 'admin' обновлен на 'Admin123!' ({result_admin.rowcount} строк)")
            print(f"[OK] Пароль для 'client' обновлен на 'Client123!' ({result_client.rowcount} строк)")
            print("\nНовые пароли соответствуют требованиям:")
            print("  - Минимум 8 символов")
            print("  - Хотя бы одна заглавная буква")
            print("  - Хотя бы одна строчная буква")
            print("  - Хотя бы одна цифра")
            print("  - Хотя бы один спецсимвол (!@#$%^&*()_-+=)")

        except Exception as e:
            await session.rollback()
            print(f"[ERROR] Ошибка при обновлении паролей: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(update_user_passwords())
