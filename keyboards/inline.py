from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def time_selection_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="09:00", callback_data="set_time_09:00"), InlineKeyboardButton(text="12:00", callback_data="set_time_12:00")],
        [InlineKeyboardButton(text="15:00", callback_data="set_time_15:00"), InlineKeyboardButton(text="18:00", callback_data="set_time_18:00")]
    ])