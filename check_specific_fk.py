"""Check specific FK for user_code_verifications"""
import asyncio
from sqlalchemy import text
from app.infrastructure.db import AsyncSessionLocal


async def check():
    async with AsyncSessionLocal() as session:
        query = text("""
            SELECT
                tc.constraint_name,
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table,
                rc.update_rule,
                rc.delete_rule,
                c.is_nullable
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON tc.constraint_name = ccu.constraint_name
            JOIN information_schema.referential_constraints rc
                ON tc.constraint_name = rc.constraint_name
            JOIN information_schema.columns c
                ON c.table_name = tc.table_name AND c.column_name = kcu.column_name
            WHERE tc.table_name = 'user_code_verifications'
                AND tc.constraint_type = 'FOREIGN KEY';
        """)

        result = await session.execute(query)
        rows = result.fetchall()

        print("Foreign Keys for user_code_verifications:")
        print("="*80)
        for row in rows:
            constraint_name, table_name, column_name, foreign_table, update_rule, delete_rule, is_nullable = row
            print(f"\nConstraint: {constraint_name}")
            print(f"  Column: {column_name} -> {foreign_table}")
            print(f"  UPDATE: {update_rule}")
            print(f"  DELETE: {delete_rule}")
            print(f"  Nullable: {is_nullable}")


if __name__ == "__main__":
    asyncio.run(check())
