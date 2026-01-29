from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from database.db import Database
from config import LOG_START
from keyboards.reply import main_menu
from datetime import datetime

router = Router()
db = Database()

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
    
    # Bazaga qo'shish
    db.add_user(user_id, full_name, username)
    
    # LOG_START kanaliga to'liq ma'lumotni bir marta yuborish
    if not db.is_start_logged(user_id):
        log_text = (
            "🆕 <b>Yangi foydalanuvchi botni ishga tushirdi!</b>\n\n"
            f"👤 <b>Ism:</b> {full_name}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"🌐 <b>Username:</b> {username}\n"
            f"📅 <b>Sana:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        try:
            await bot.send_message(LOG_START, log_text, parse_mode="HTML")
            db.set_start_logged(user_id)
        except Exception as e:
            print(f"Start log xatosi: {e}")
        
    await message.answer(
        f"Assalomu alaykum, {full_name}! 👋\n"
        f"<b>ATKO</b> o'quv markazining rasmiy botiga xush kelibsiz.\n\n"
        f"Kurslarimiz va xizmatlarimiz bilan tanishish uchun bo'limni tanlang: 👇", 
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@router.message(F.text == "🏫 O'quv markaz haqida")
async def about_center(message: types.Message):
    await message.answer("<b>ATKO O'quv Markazi</b> 🎓\n\nBiz 5 yildan buyon koreys tili bo'yicha sifatli ta'lim berib kelmoqdamiz.")

@router.message(F.text == "🕒 Ish vaqti")
async def work_hours(message: types.Message):
    await message.answer("🕒 <b>Ish tartibimiz:</b>\n\n📅 Dush-Shanba\n⏰ 09:00 - 19:00")

@router.message(F.text == "📍 Joylashuv")
async def location(message: types.Message):
    await message.answer("📍 <b>Manzil:</b> Namangan viloyati, Kurghay tumani.")

@router.message(F.text == "👨‍💻 Admin bilan bog'lanish")
async def contact_admin(message: types.Message):
    await message.answer("👨‍💻 <b>Admin:</b> @atko_admin_user\n📞 +998 90 123 45 67")