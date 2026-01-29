from datetime import datetime
from aiogram import Bot, types
from database.db import Database
from config import PRIVATE_CONTENT_GROUP_ID, LOG_STATS
from utils.excel_gen import generate_excel_report

db = Database()

async def check_and_send_lessons(bot: Bot):
    # Har soat boshida ishlaydi (soat:00)
    now_time = datetime.now().strftime("%H:00")
    users = db.get_users_for_lesson(now_time)
    
    for user_id, current_lesson in users:
        next_lesson = current_lesson + 1
        msg_id = db.get_lesson_msg_id(next_lesson)
        
        if msg_id:
            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=PRIVATE_CONTENT_GROUP_ID,
                    message_id=msg_id,
                    protect_content=True
                )
                db.update_lesson_progress(user_id, next_lesson)
            except Exception as e:
                print(f"User {user_id} ga dars yuborilmadi: {e}")

async def send_daily_reports(bot: Bot):
    # Har kuni 09:00 da hisobot yuborish
    total, with_phone, no_phone = db.get_stats()
    file_path = generate_excel_report()
    
    report_text = (
        "📊 <b>Kunlik CRM Statistika</b>\n\n"
        f"👥 Jami: {total}\n"
        f"✅ Tel raqamli: {with_phone}\n"
        f"❌ Tel raqamsiz: {no_phone}"
    )
    
    try:
        await bot.send_message(LOG_STATS, report_text, parse_mode="HTML")
        if file_path:
            await bot.send_document(
                LOG_STATS, 
                types.FSInputFile(file_path), 
                caption="📁 O'quvchilar ro'yxati (Excel)"
            )
    except Exception as e:
        print(f"Hisobot yuborishda xato: {e}")