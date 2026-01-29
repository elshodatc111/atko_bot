from aiogram import Router, F, types
from database.db import Database
from keyboards.inline import time_selection_kb
from keyboards.reply import phone_btn

router = Router()
db = Database()

@router.message(F.text == "📚 Kurslar")
async def show_courses(message: types.Message):
    await message.answer("Koreys tili kursi. Boshlash uchun tel yuboring:", reply_markup=phone_btn())

@router.callback_query(F.data == "next_lesson_1")
async def next_info(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) # Tugmani o'chirish
    await callback.message.answer("Darslarni har kuni qaysi vaqtda yuboraylik?", reply_markup=time_selection_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("set_time_"))
async def save_time(callback: types.CallbackQuery):
    t = callback.data.replace("set_time_", "")
    db.set_user_time(callback.from_user.id, t)
    await callback.message.edit_text(f"✅ Saqlandi! Har kuni {t} da dars yuboriladi.")
    await callback.answer()