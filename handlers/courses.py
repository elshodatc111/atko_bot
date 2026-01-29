from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from config import PRIVATE_CONTENT_GROUP_ID
from keyboards.inline import time_selection_kb
from keyboards.reply import phone_btn

router = Router()
db = Database()

# --- YORDAMCHI FUNKSIYA: DARSLAR ARXIVI TUGMALARI ---
def get_lesson_history_kb(current_lesson):
    buttons = []
    row = []
    for i in range(1, current_lesson + 1):
        row.append(InlineKeyboardButton(text=f"📖 {i}-dars", callback_data=f"view_lesson_{i}"))
        if len(row) == 2: # Bir qatorda 2 tadan tugma chiqishi uchun
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    
    # Vaqtni o'zgartirish tugmasini ham qo'shimcha sifatida qo'shish mumkin
    buttons.append([InlineKeyboardButton(text="🕓 Dars vaqtini o'zgartirish", callback_data="change_my_time")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ASOSIY HANDLER: KURSLAR BO'LIMI ---
@router.message(F.text == "📚 Kurslar")
async def show_courses(message: types.Message, bot: Bot):
    user_info = db.get_user_info(message.from_user.id)
    
    # 1. AGAR FOYDALANUVCHI RO'YXATDAN O'TMAGAN BO'LSA (TELEFON YO'Q)
    if not user_info or not user_info[0]:
        marketing_caption = (
            "🎓 <b>ATKO: Koreys tili kursiga xush kelibsiz!</b>\n\n"
            "Siz bu yerda koreys tilini mutlaqo <b>BEPUL</b> va professional tizim asosida o'rganasiz. "
            "Bizning botimiz shunchaki ma'lumotlar ombori emas, u sizning shaxsiy repetitoringizdir.\n\n"
            "🚀 <b>Bot qanday ishlaydi?</b>\n"
            "1️⃣ <b>Ro'yxatdan o'tasiz:</b> Telefon yuboring va darhol <b>1-DARS</b>ni oling.\n"
            "2️⃣ <b>Bilimni mustahkamlaysiz:</b> Darslar miyaga sifatli singishi uchun har kuni <b>1 tadan</b> yuboriladi.\n"
            "3️⃣ <b>Vaqtni o'zingiz boshqarasiz:</b> Darslar aynan siz tanlagan vaqtda yuboriladi.\n\n"
            "👇 <b>Boshlash uchun pastdagi tugmani bosib, telefon raqamingizni yuboring:</b>"
        )
        return await message.answer(marketing_caption, reply_markup=phone_btn(), parse_mode="HTML")

    # 2. AGAR FOYDALANUVCHI ALLAQACHON RO'YXATDAN O'TGAN BO'LSA
    phone, current_lesson, send_time = user_info
    next_lesson = current_lesson + 1
    
    if current_lesson == 0:
        return await message.answer("✅ Ro'yxatdan o'tgansiz. Tez orada birinchi darsingiz yuboriladi!")

    # Keyingi dars haqida ma'lumot
    time_info = f"🕓 Keyingi <b>{next_lesson}-darsingiz</b> ertaga soat <b>{send_time}</b> da yuboriladi." if send_time else "⚠️ Dars vaqti belgilanmagan."

    caption = (
        "📊 <b>Sizning o'quv natijangiz:</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>O'zlashtirilgan darslar:</b> {current_lesson} ta\n"
        f"{time_info}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "📚 <b>Darslar arxivi:</b>\n"
        "Pastdagi tugmalar orqali o'tilgan darslarni istalgan payt takrorlashingiz mumkin:"
    )

    last_msg_id = db.get_lesson_msg_id(current_lesson)
    
    if last_msg_id:
        # Oxirgi dars videosini yuborish va tarix tugmalarini ilova qilish
        await bot.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=PRIVATE_CONTENT_GROUP_ID,
            message_id=last_msg_id,
            protect_content=True,
            caption=caption,
            reply_markup=get_lesson_history_kb(current_lesson),
            parse_mode="HTML"
        )
    else:
        await message.answer(caption, reply_markup=get_lesson_history_kb(current_lesson), parse_mode="HTML")

# --- CALLBACK: TARIXDAGI DARSLARNI KO'RISH ---
@router.callback_query(F.data.startswith("view_lesson_"))
async def view_old_lesson(callback: types.CallbackQuery, bot: Bot):
    lesson_num = int(callback.data.replace("view_lesson_", ""))
    msg_id = db.get_lesson_msg_id(lesson_num)
    
    if msg_id:
        await bot.copy_message(
            chat_id=callback.from_user.id,
            from_chat_id=PRIVATE_CONTENT_GROUP_ID,
            message_id=msg_id,
            protect_content=True,
            caption=f"📚 <b>{lesson_num}-dars (Takrorlash darsi)</b>",
            parse_mode="HTML"
        )
        await callback.answer(f"{lesson_num}-dars yuborildi.")
    else:
        await callback.answer("Dars topilmadi.", show_alert=True)

# --- CALLBACK: 1-DARSDAN KEYIN VAQT TANLASH ---
@router.callback_query(F.data == "next_lesson_1")
async def ask_time(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "🎯 <b>Ajoyib boshlanish!</b>\n\n"
        "Darslar har kuni tartibli kelishi uchun o'zingizga qulay vaqtni tanlang. "
        "Bot har kuni aynan shu vaqtda yangi darsni sizga yetkazadi: 👇",
        reply_markup=time_selection_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

# --- CALLBACK: VAQTNI SAQLASH ---
@router.callback_query(F.data.startswith("set_time_"))
async def save_time(callback: types.CallbackQuery):
    t = callback.data.replace("set_time_", "")
    db.set_user_time(callback.from_user.id, t)
    await callback.message.edit_text(
        f"✅ <b>Vaqt saqlandi!</b>\n\n"
        f"Endi har kuni soat <b>{t}</b> da sizga yangi dars videosi yuboriladi. "
        "Bilim olishda muntazamlik eng muhimi!",
        parse_mode="HTML"
    )
    await callback.answer()

# --- CALLBACK: VAQTNI O'ZGARTIRISH TUGMASI ---
@router.callback_query(F.data == "change_my_time")
async def change_time(callback: types.CallbackQuery):
    await callback.message.answer("Yangi dars yuborish vaqtini tanlang:", reply_markup=time_selection_kb())
    await callback.answer()