"""Check for NULL user_id in user_code_verifications"""
import asyncio
from sqlalchemy import text
from app.infrastructure.db import AsyncSessionLocal


async def check():
    async with AsyncSessionLocal() as session:
        # Check for NULL user_id
        query1 = text("""
            SELECT id, user_id, code, created_at, expired_at
            FROM user_code_verifications
            WHERE user_id IS NULL;
        """)

        result1 = await session.execute(query1)
        rows1 = result1.fetchall()

        print("Records with NULL user_id:")
        print("="*80)
        if rows1:
            for row in rows1:
                print(f"ID: {row[0]}, user_id: {row[1]}, code: {row[2]}, created: {row[3]}")
            print(f"\nTotal: {len(rows1)} records with NULL user_id")
        else:
            print("No records with NULL user_id found")

        # Check total records
        query2 = text("SELECT COUNT(*) FROM user_code_verifications;")
        result2 = await session.execute(query2)
        total = result2.scalar()

        print(f"\nTotal records in user_code_verifications: {total}")

        # Check record with id=10 (from error message)
        query3 = text("""
            SELECT id, user_id, code, created_at, expired_at, updated_at
            FROM user_code_verifications
            WHERE id = 10;
        """)

        result3 = await session.execute(query3)
        row = result3.fetchone()

        print("\nRecord with id=10:")
        print("="*80)
        if row:
            print(f"ID: {row[0]}")
            print(f"user_id: {row[1]}")
            print(f"code: {row[2]}")
            print(f"created_at: {row[3]}")
            print(f"expired_at: {row[4]}")
            print(f"updated_at: {row[5]}")
        else:
            print("No record with id=10")


if __name__ == "__main__":
    asyncio.run(check())
