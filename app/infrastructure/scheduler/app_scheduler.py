import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from app.infrastructure.db import AsyncSessionLocal
from app.use_case.booking_field_party_request.scheduler.check_booking_field_party_request_case import \
    CheckBookingFieldPartyRequestCase
from app.use_case.product_order.scheduler.check_product_order_payment_case import CheckProductOrderPaymentCase
from app.use_case.ticketon_order.scheduler.check_ticketon_order_case import CheckTicketonOrderTimeCase

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")


# Универсальный шаблон для выполнения UseCase
async def run_use_case(use_case_cls, log_success: str, log_error: str):
    try:
        async with AsyncSessionLocal() as session:
            use_case = use_case_cls(session)
            await use_case.execute()
        logger.info(log_success)
    except Exception as exc:
        logger.error(f"{log_error}: {exc}")


# --- Твои задачи ---
async def check_product_order_payment_process():
    await run_use_case(
        CheckProductOrderPaymentCase,
        "check_product_order_payment_process: Проверка оплат заказов завершена.",
        "check_product_order_payment_process: Ошибка при проверке оплат заказов",
    )


async def check_booking_field_party_request_process():
    await run_use_case(
        CheckBookingFieldPartyRequestCase,
        "check_booking_field_party_request_process: Проверка бронирований завершена.",
        "check_booking_field_party_request_process: Ошибка при проверке бронирований",
    )


async def check_ticketon_order_time_process():
    await run_use_case(
        CheckTicketonOrderTimeCase,
        "check_ticketon_order_time_process: Проверка заказов Ticketon завершена.",
        "check_ticketon_order_time_process: Ошибка при проверке заказов Ticketon",
    )


# Listener для всех задач
def job_listener(event):
    if event.exception:
        logger.error(f"Ошибка в задаче {event.job_id}: {event.exception}")
    else:
        logger.info(f"Задача {event.job_id} успешно завершена")


# Основной цикл
async def main():
    scheduler = AsyncIOScheduler()

    # Все три задачи выполняются ежеминутно
    scheduler.add_job(
        check_product_order_payment_process,
        "interval",
        minutes=1,
        id="check_product_order_payment",
    )
    scheduler.add_job(
        check_booking_field_party_request_process,
        "interval",
        minutes=1,
        id="check_booking_field_party_request",
    )
    scheduler.add_job(
        check_ticketon_order_time_process,
        "interval",
        minutes=1,
        id="check_ticketon_order_time",
    )

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    logger.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping scheduler...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
