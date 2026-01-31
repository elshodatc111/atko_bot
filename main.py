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

# Bot obyekti (global yoki funksiya ichida)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

async def run_scheduler_once():
    """Faqat Scheduled Task uchun: Darslarni bir marta yuboradi va to'xtaydi"""
    print("\n⏰ Scheduled Task: Darslar tekshirilmoqda...")
    try:
        # Darslarni yuborish funksiyasini bir marta chaqiramiz
        await check_and_send_lessons(bot)
        # Agar soat 9 bo'lsa, hisobotni ham yuborish (ixtiyoriy)
        await send_daily_reports(bot)
        print("✅ Darslar yuborildi.")
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
    finally:
        await bot.session.close()

async def main():
    """Service (User Program) uchun: Botni doimiy polling rejimida yoqadi"""
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_routers(start.router, contact.router, courses.router, admin_post.router)

    # Scheduler sozlamalari (Service yoniq turganda ham fonda ishlayveradi)
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    # Har soatning boshida (0-daqiqada) tekshirish
    scheduler.add_job(check_and_send_lessons, "cron", minute=0, args=[bot])
    scheduler.add_job(send_daily_reports, "cron", hour=9, minute=0, args=[bot])
    scheduler.start()

    print("\n🚀 Bot Service ishga tushdi...")
    try:
        try:
            await bot.send_message(LOG_START, "✅ <b>Bot tizimi (Service) ishga tushdi!</b>")
        except Exception as e:
            print(f"Log xabari yuborilmadi: {e}")
            
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Agar buyruq --send-lessons bilan berilgan bo'lsa
    if "--send-lessons" in sys.argv:
        asyncio.run(run_scheduler_once())
    else:
        # Oddiy ishga tushirish (Service uchun)
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            print("\n🛑 Bot to'xtatildi!")