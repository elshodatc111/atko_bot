from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from config import LOG_PHONE_1, PRIVATE_CONTENT_GROUP_ID
from keyboards.reply import main_menu # Asosiy menyuni chaqiramiz

router = Router()
db = Database()

@router.message(F.contact)
async def handle_contact(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    phone = message.contact.phone_number
    full_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    # 1. Ma'lumotlarni bazada yangilash
    db.update_phone(user_id, phone)
    
    # 2. Kanalga log yuborish (faqat bir marta)
    if not db.is_phone_logged(user_id):
        phone_log = (
            "📱 <b>Yangi o'quvchi ro'yxatdan o'tdi!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📞 <b>Tel:</b> {phone}\n"
            f"👤 <b>Ism:</b> {full_name}\n"
            f"🌐 <b>Username:</b> {username}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>"
        )
        try:
            await bot.send_message(LOG_PHONE_1, phone_log, parse_mode="HTML")
            db.set_phone_logged(user_id)
        except Exception as e:
            print(f"Log yuborishda xato: {e}")

    # 3. 1-dars videosini yuborish
    msg_id = db.get_lesson_msg_id(1)
    if msg_id:
        # Video ostidagi dars tugmasi
        lesson_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⏭ Keyingi darsni olish", callback_data="next_lesson_1")]
        ])
        
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=PRIVATE_CONTENT_GROUP_ID,
            message_id=msg_id,
            protect_content=True,
            reply_markup=lesson_kb
        )
        db.update_lesson_progress(user_id, 1)

        # 4. ASOSIY MENYUNI CHIQARISH (Siz so'ragan qism)
        success_text = (
            "✅ <b>Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.</b>\n\n"
            "Yuqorida siz uchun 1-dars videosi yuborildi. Uni ko'rib bo'lgach, "
            "<b>'Keyingi dars'</b> tugmasini bosing.\n\n"
            "Pastdagi menyu orqali markazimiz haqida ma'lumot olishingiz mumkin: 👇"
        )
        await message.answer(success_text, reply_markup=main_menu(), parse_mode="HTML")
        
    else:
        # Agar baza dars qo'shilmagan bo'lsa
        await message.answer(
            "✅ Ma'lumotlaringiz qabul qilindi! Tez orada darslar yuklanadi.", 
            reply_markup=main_menu()
        )