import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, LOG_START
from handlers import start, contact, courses, admin_post
from utils.scheduler import check_and_send_lessons, send_daily_reports

# Loglarni sozlash
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_routers(start.router, contact.router, courses.router, admin_post.router)

    # Scheduler sozlamalari
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(check_and_send_lessons, "cron", minute=0, args=[bot])
    scheduler.add_job(send_daily_reports, "cron", hour=9, minute=0, args=[bot])
    scheduler.start()

    # Bot yoqilgani haqida xabar
    print("\n🚀 Bot ishga tushdi...")
    try:
        await bot.send_message(LOG_START, "✅ <b>Bot tizimi ishga tushdi!</b>")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Windows uchun maxsus xatolikni oldini olish
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot to'xtatildi!")