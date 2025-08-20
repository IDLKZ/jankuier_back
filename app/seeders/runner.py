from app.infrastructure.db import AsyncSessionLocal
from app.seeders.registry import seeders


async def run_seeders() -> None:
    """Запускает все сидеры."""
    async with AsyncSessionLocal() as session:
        for seeder in seeders:
            await seeder.seed(session)
