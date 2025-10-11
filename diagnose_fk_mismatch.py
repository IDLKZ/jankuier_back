"""
Расширенная диагностика Foreign Keys - поиск несоответствий между моделями и БД.

Проверяет:
1. FK с SET NULL на NOT NULL полях (критическая ошибка)
2. FK с неправильными constraints
3. Несоответствие между nullable в модели и реальным constraint в БД

Использование:
    python diagnose_fk_mismatch.py
"""
import asyncio
from sqlalchemy import text, inspect
from sqlalchemy.orm import DeclarativeMeta
from app.infrastructure.db import AsyncSessionLocal, Base, engine_async
from app.shared.db_table_constants import AppTableNames


async def get_db_foreign_keys():
    """Получить все FK из БД с их constraints"""
    async with AsyncSessionLocal() as session:
        query = text("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.update_rule,
                rc.delete_rule,
                c.is_nullable
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
            JOIN information_schema.columns AS c
                ON c.table_name = tc.table_name
                AND c.column_name = kcu.column_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            ORDER BY tc.table_name, kcu.column_name;
        """)

        result = await session.execute(query)
        rows = result.fetchall()

        fk_map = {}
        for row in rows:
            table, column, foreign_table, foreign_column, update_rule, delete_rule, is_nullable = row
            fk_map[f"{table}.{column}"] = {
                'table': table,
                'column': column,
                'foreign_table': foreign_table,
                'foreign_column': foreign_column,
                'update_rule': update_rule,
                'delete_rule': delete_rule,
                'is_nullable': is_nullable == 'YES'
            }

        return fk_map


def get_model_foreign_keys():
    """Получить все FK из моделей SQLAlchemy"""
    fk_model_map = {}

    # Получаем все модели из Base
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        table_name = model_class.__tablename__

        # Проходим по всем столбцам
        for column in mapper.columns:
            # Проверяем, есть ли foreign key
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    column_name = column.name
                    key = f"{table_name}.{column_name}"

                    fk_model_map[key] = {
                        'table': table_name,
                        'column': column_name,
                        'nullable': column.nullable,
                        'model_ondelete': getattr(fk, 'ondelete', None),
                        'model_onupdate': getattr(fk, 'onupdate', None),
                    }

    return fk_model_map


async def diagnose():
    """Главная функция диагностики"""
    print("="*100)
    print("FOREIGN KEY MISMATCH DIAGNOSIS")
    print("="*100 + "\n")

    print("Loading FK from database...")
    db_fks = await get_db_foreign_keys()

    print("Loading FK from SQLAlchemy models...")
    model_fks = get_model_foreign_keys()

    print(f"\nFound {len(db_fks)} FK in database")
    print(f"Found {len(model_fks)} FK in models\n")

    # Категории проблем
    critical_errors = []  # SET NULL на NOT NULL полях
    warnings = []  # Несоответствия между моделью и БД
    info = []  # Информационные сообщения

    # Проверка каждого FK
    for key, db_fk in db_fks.items():
        model_fk = model_fks.get(key)

        # Критическая ошибка: SET NULL на NOT NULL поле
        if db_fk['delete_rule'] == 'SET NULL' and not db_fk['is_nullable']:
            critical_errors.append({
                'key': key,
                'db_fk': db_fk,
                'model_fk': model_fk,
                'reason': 'SET NULL on NOT NULL field - will cause NotNullViolationError'
            })

        # Проверка несоответствия с моделью
        if model_fk:
            # Несоответствие nullable
            if model_fk['nullable'] != db_fk['is_nullable']:
                warnings.append({
                    'key': key,
                    'db_fk': db_fk,
                    'model_fk': model_fk,
                    'reason': f"Nullable mismatch: model={model_fk['nullable']}, db={db_fk['is_nullable']}"
                })

            # Несоответствие ondelete
            if model_fk['model_ondelete'] and model_fk['model_ondelete'] != db_fk['delete_rule']:
                warnings.append({
                    'key': key,
                    'db_fk': db_fk,
                    'model_fk': model_fk,
                    'reason': f"ondelete mismatch: model={model_fk['model_ondelete']}, db={db_fk['delete_rule']}"
                })

    # Вывод критических ошибок
    if critical_errors:
        print("="*100)
        print("CRITICAL ERRORS (MUST FIX):")
        print("="*100)
        for error in critical_errors:
            print(f"\n[CRITICAL] {error['key']}")
            print(f"  Table: {error['db_fk']['table']}")
            print(f"  Column: {error['db_fk']['column']} -> {error['db_fk']['foreign_table']}.{error['db_fk']['foreign_column']}")
            print(f"  DB: DELETE {error['db_fk']['delete_rule']}, nullable={error['db_fk']['is_nullable']}")
            if error['model_fk']:
                print(f"  Model: nullable={error['model_fk']['nullable']}, ondelete={error['model_fk']['model_ondelete']}")
            print(f"  Problem: {error['reason']}")
            print(f"  Fix: Change ondelete to CASCADE or RESTRICT, or make field nullable")
        print()

    # Вывод предупреждений
    if warnings:
        print("="*100)
        print("WARNINGS (Model/DB mismatch):")
        print("="*100)
        for warning in warnings:
            print(f"\n[WARNING] {warning['key']}")
            print(f"  Table: {warning['db_fk']['table']}")
            print(f"  DB: DELETE {warning['db_fk']['delete_rule']}, nullable={warning['db_fk']['is_nullable']}")
            if warning['model_fk']:
                print(f"  Model: nullable={warning['model_fk']['nullable']}, ondelete={warning['model_fk']['model_ondelete']}")
            print(f"  Problem: {warning['reason']}")
        print()

    # Итоговая статистика
    print("="*100)
    print("SUMMARY:")
    print("="*100)
    print(f"Critical Errors: {len(critical_errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Total FK checked: {len(db_fks)}")
    print()

    if critical_errors:
        print("ACTION REQUIRED:")
        print("1. Fix critical errors - these WILL cause NotNullViolationError on delete")
        print("2. Create migration to fix FK constraints")
        print("3. Or update models to match database constraints")
        print()
        return False
    elif warnings:
        print("RECOMMENDATIONS:")
        print("1. Review warnings - models and DB are out of sync")
        print("2. Consider creating migration to align constraints")
        print()
        return True
    else:
        print("All FK constraints are correct!")
        return True


def main():
    result = asyncio.run(diagnose())
    if not result:
        exit(1)


if __name__ == "__main__":
    main()
