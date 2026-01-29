import asyncio
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_IDS, LOG_PHONE_2, PRIVATE_CONTENT_GROUP_ID
from database.db import Database
from utils.excel_gen import generate_excel_report

router = Router()
db = Database()

class PostState(StatesGroup):
    waiting_for_audience = State()
    waiting_for_content = State()

class LessonState(StatesGroup):
    waiting_for_lesson_num = State()

# --- REKLAMA TIZIMI ---
@router.message(Command("post"))
async def start_post(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS: return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Barcha", callback_data="target_all")],
        [InlineKeyboardButton(text="📱 Tel borlar", callback_data="target_with_phone")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="post_cancel")]
    ])
    await message.answer("📢 <b>Reklama:</b> Auditoriyani tanlang:", reply_markup=kb, parse_mode="HTML")
    await state.set_state(PostState.waiting_for_audience)

@router.callback_query(F.data.startswith("target_"))
async def select_target(callback: types.CallbackQuery, state: FSMContext):
    target = callback.data.replace("target_", "")
    await state.update_data(target=target)
    await callback.message.edit_text("📥 <b>Postni yuboring:</b>\n(Matn, rasm yoki video ko'rinishida)", parse_mode="HTML")
    await state.set_state(PostState.waiting_for_content)

@router.message(PostState.waiting_for_content)
async def get_content(message: types.Message, state: FSMContext):
    if message.text: 
        await state.update_data(m_type="text", content=message.text, caption="")
    elif message.photo: 
        await state.update_data(m_type="photo", content=message.photo[-1].file_id, caption=message.caption or "")
    elif message.video: 
        await state.update_data(m_type="video", content=message.video.file_id, caption=message.caption or "")
    else:
        await message.answer("❌ Noto'g'ri format. Iltimos, matn, rasm yoki video yuboring.")
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash va Yuborish", callback_data="post_confirm")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="post_cancel")]
    ])
    await message.answer("📝 <b>Post tayyor.</b> Uni barchaga yuborishni tasdiqlaysizmi?", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "post_confirm")
async def send_broadcast(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    users = db.get_audience(data['target'])
    
    # Post yuborayotgan admin ma'lumotlari
    admin_name = callback.from_user.full_name
    admin_username = f"@{callback.from_user.username}" if callback.from_user.username else "Mavjud emas"
    admin_id = callback.from_user.id

    await callback.message.edit_text(f"🚀 {len(users)} kishiga yuborish boshlandi...")
    
    success, fail = 0, 0
    for user in users:
        try:
            if data['m_type'] == "text": 
                await bot.send_message(user[0], data['content'])
            elif data['m_type'] == "photo": 
                await bot.send_photo(user[0], data['content'], caption=data['caption'])
            elif data['m_type'] == "video": 
                await bot.send_video(user[0], data['content'], caption=data['caption'])
            success += 1
            await asyncio.sleep(0.05) # Telegram limitlari uchun
        except: 
            fail += 1

    # 3-kanal (LOG_PHONE_2) uchun to'liq hisobot
    report = (
        "📢 <b>Reklama Tarqatish Hisoboti</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Admin:</b> {admin_name}\n"
        f"🌐 <b>Username:</b> {admin_username}\n"
        f"🆔 <b>Admin ID:</b> <code>{admin_id}</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Maqsadli guruh:</b> {data['target']}\n"
        f"✅ <b>Muvaffaqiyatli:</b> {success}\n"
        f"❌ <b>Xatoliklar:</b> {fail}\n"
        f"📊 <b>Jami urinish:</b> {len(users)}"
    )

    # LOG_PHONE_2 kanaliga ham postni, ham hisobotni yuboramiz
    try:
        if data['m_type'] == "text": 
            await bot.send_message(LOG_PHONE_2, f"📢 <b>Yuborilgan post:</b>\n\n{data['content']}\n\n{report}", parse_mode="HTML")
        elif data['m_type'] == "photo": 
            await bot.send_photo(LOG_PHONE_2, data['content'], caption=f"{data['caption']}\n\n{report}", parse_mode="HTML")
        elif data['m_type'] == "video": 
            await bot.send_video(LOG_PHONE_2, data['content'], caption=f"{data['caption']}\n\n{report}", parse_mode="HTML")
    except Exception as e:
        print(f"Admin log yuborishda xato: {e}")

    await callback.message.answer(f"✅ Reklama yakunlandi!\nMuvaffaqiyatli: {success}")
    await state.clear()

# --- DARSLARNI QO'SHISH ---
@router.message(F.video | F.document)
async def admin_save_lesson(message: types.Message, state: FSMContext):
    # Admin dars videosini yopiq guruhdan forward qilsa
    if message.from_user.id in ADMIN_IDS and message.forward_from_chat:
        if message.forward_from_chat.id == PRIVATE_CONTENT_GROUP_ID:
            await state.update_data(m_id=message.forward_from_message_id)
            await message.answer("🔢 <b>Bu nechanchi dars?</b>\nFaqat raqam yuboring (masalan: 5):", parse_mode="HTML")
            await state.set_state(LessonState.waiting_for_lesson_num)

@router.message(LessonState.waiting_for_lesson_num)
async def finalize_lesson(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, faqat raqam yuboring!")
        return
        
    d = await state.get_data()
    db.add_lesson(int(message.text), d['m_id'], f"{message.text}-dars")
    await message.answer(f"✅ <b>{message.text}-dars</b> muvaffaqiyatli bazaga qo'shildi!", parse_mode="HTML")
    await state.clear()

@router.message(Command("get_excel"))
async def admin_excel_request(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        path = generate_excel_report()
        if path:
            await message.answer_document(types.FSInputFile(path), caption="📁 <b>Joriy o'quvchilar bazasi</b>", parse_mode="HTML")

@router.callback_query(F.data == "post_cancel")
async def cancel_operation(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Amaliyot bekor qilindi.")