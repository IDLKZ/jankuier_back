"""
Утилита для проверки Foreign Key constraints в базе данных PostgreSQL.

Проверяет соответствие CASCADE constraints между моделями SQLAlchemy и реальной схемой БД.

Использование:
    python check_foreign_keys.py              # Проверка и отчет
    python check_foreign_keys.py --strict     # Проверка с exit code 1 при ошибках (для CI/CD)

Автор: Generated for JanKuier Project
Дата: 2025-10-11
"""
import asyncio
import sys
from sqlalchemy import text
from app.infrastructure.db import AsyncSessionLocal


async def check_foreign_keys(strict_mode: bool = False):
    """
    Проверка всех foreign keys в БД.

    Args:
        strict_mode: Если True, завершится с exit code 1 при наличии ошибок
    """
    async with AsyncSessionLocal() as session:
        query = text("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.update_rule,
                rc.delete_rule
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            JOIN information_schema.referential_constraints AS rc
                ON rc.constraint_name = tc.constraint_name
                AND rc.constraint_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            ORDER BY tc.table_name, kcu.column_name;
        """)

        result = await session.execute(query)
        rows = result.fetchall()

        print("\n" + "="*100)
        print("FOREIGN KEYS WITHOUT CASCADE ON DELETE:")
        print("="*100)

        no_cascade_count = 0
        for row in rows:
            table, column, foreign_table, foreign_column, update_rule, delete_rule = row

            if delete_rule != 'CASCADE':
                no_cascade_count += 1
                print(f"\n[!] {table}.{column} -> {foreign_table}.{foreign_column}")
                print(f"   UPDATE: {update_rule}, DELETE: {delete_rule}")

        print(f"\n{'='*100}")
        print(f"Total FK without CASCADE: {no_cascade_count} out of {len(rows)}")
        print("="*100 + "\n")

        if no_cascade_count > 0:
            print("RECOMMENDATIONS:")
            print("1. Run migration: alembic upgrade head")
            print("2. If migration already applied, check docs/foreign_key_cascade_guide.md")
            print("3. Review entity models for correct ondelete settings")
            print()

        if strict_mode and no_cascade_count > 0:
            print("ERROR: Found FK constraints without proper CASCADE settings!")
            print("       Exiting with error code for CI/CD pipeline.")
            return False

        return no_cascade_count == 0


def main():
    """Main entry point with CLI argument handling."""
    strict_mode = "--strict" in sys.argv or "-s" in sys.argv

    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    result = asyncio.run(check_foreign_keys(strict_mode=strict_mode))

    if strict_mode and not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
