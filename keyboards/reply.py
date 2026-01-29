from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🏫 O'quv markaz haqida"), KeyboardButton(text="📚 Kurslar")],
        [KeyboardButton(text="🕒 Ish vaqti"), KeyboardButton(text="📍 Joylashuv")],
        [KeyboardButton(text="👨‍💻 Admin bilan bog'lanish")]
    ], resize_keyboard=True)

def phone_btn():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ], resize_keyboard=True)