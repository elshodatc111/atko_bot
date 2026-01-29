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
        f"Assalomu alaykum, {full_name}! 👋\n\n"
        f"<b>ATKO O‘quv Markazi</b>ning rasmiy botiga xush kelibsiz! 🎓\n\n"
        f"9+ yillik tajribaga ega markazimizda siz koreys tilini zamonaviy metodika va tajribali ustozlar yordamida o‘rganishingiz mumkin.\n\n"
        f"Bizning maqsadimiz — sizga shunchaki bilim berish emas, balki aniq <b>natijaga olib chiqish</b>.\n\n"
        f"📚 Kurslarimiz haqida batafsil ma’lumot olish va xizmatlarimiz bilan tanishish uchun quyidagi bo‘limlardan birini tanlang 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "🏫 O'quv markaz haqida")
async def about_center(message: types.Message):
    await message.answer(
            "<b>ATKO O'quv Markazi</b> 🎓\n\n"
            "9+ yillik tajribaga ega ATKO o‘quv markazi koreys tilini o‘rganishda ishonchli hamkoringiz hisoblanadi. "
            "Biz zamonaviy metodika va kuchli ustozlar jamoasi orqali har bir o‘quvchini real natijaga olib chiqishni maqsad qilganmiz.\n\n"
            "Bugungi kunga qadar ko‘plab bitiruvchilarimiz tilni muvaffaqiyatli egallab, o‘z orzulari sari muhim qadam tashlashdi.\n\n"
            "📌 Biz sizga shunchaki bilim emas — natijaga olib boruvchi samarali ta’limni taklif etamiz.\n\n"
            "🔹 Tajribali ustozlar\n"
            "🔹 12 kishilik kichik guruhlar\n"
            "🔹 Qulay va zamonaviy o‘quv muhit\n"
            "🔹 Online va offline kurslar\n"
            "🔹 Bepul video darslar platformasi\n\n"
            "ATKO bilan kelajagingiz sari ishonch bilan qadam tashlang!"
        )


@router.message(F.text == "🕒 Ish vaqti")
async def work_hours(message: types.Message):
    await message.answer(
            "🕒 <b>Ish vaqtimiz:</b>\n\n"
            "📅 <b>Dushanbadan Shanbagacha</b>\n"
            "⏰ <b>08:00 dan 20:00 gacha</b>\n\n"
            "ATKO o‘quv markazi sizni har kuni zamonaviy va qulay muhitda kutib olishga tayyor! 🎓"
        )


@router.message(F.text == "📍 Joylashuv")
async def location(message: types.Message):
    await message.answer(
            "📍 <b>Bizning manzil:</b>\n\n"
            "Qarshi shahri, Mustaqillik shoh ko‘chasi, 2-uy.\n"
            "📌 Mo‘ljal: Viloyat hokimligi ro‘parasida.\n\n"
            "Sizni zamonaviy o‘quv markazimizda kutib qolamiz! 🎓"
        )


@router.message(F.text == "👨‍💻 Admin bilan bog'lanish")
async def contact_admin(message: types.Message):
    await message.answer(
            "📞 <b>Bog‘lanish uchun:</b>\n\n"
            "☎️ <b>Telefon:</b> +998 91 950 11 01\n"
            "💬 <b>Telegram:</b> <a href='https://t.me/atko001'>@atko001</a>\n\n"
            "Savollaringiz bo‘lsa, bemalol murojaat qiling — sizga yordam berishdan mamnunmiz! 😊"
        )
