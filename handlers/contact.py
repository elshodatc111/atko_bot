from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from config import LOG_PHONE_1, PRIVATE_CONTENT_GROUP_ID

router = Router()
db = Database()

@router.message(F.contact)
async def handle_contact(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    phone = message.contact.phone_number
    full_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"

    db.update_phone(user_id, phone)
    
    # Faqat LOG_PHONE_1 kanaliga bir marta yuborish
    if not db.is_phone_logged(user_id):
        phone_log = (
            "📱 <b>Yangi o'quvchi ro'yxatdan o'tdi!</b>\n\n"
            f"📞 <b>Tel:</b> {phone}\n"
            f"👤 <b>Ism:</b> {full_name}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"🌐 <b>Username:</b> {username}"
        )
        try:
            await bot.send_message(LOG_PHONE_1, phone_log, parse_mode="HTML")
            db.set_phone_logged(user_id)
        except Exception as e:
            print(f"Phone log xatosi: {e}")

    # 1-dars videosini yuborish
    msg_id = db.get_lesson_msg_id(1)
    if msg_id:
        await message.answer("✅ Raxmat! 1-dars videosi yuborilmoqda...", reply_markup=types.ReplyKeyboardRemove())
        await bot.copy_message(
            chat_id=user_id, 
            from_chat_id=PRIVATE_CONTENT_GROUP_ID, 
            message_id=msg_id, 
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⏭ Keyingi darsni olish", callback_data="next_lesson_1")]])
        )
        db.update_lesson_progress(user_id, 1)
    else:
        await message.answer("✅ Tel saqlandi. Darslar tez orada yuklanadi.")