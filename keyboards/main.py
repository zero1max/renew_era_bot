from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(is_admin=False):
    keyboard = [
        [KeyboardButton(text="Bilimni sinash")]
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="View Results")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_question_keyboard(options):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=option, callback_data=f"answer_{i}")]
        for i, option in enumerate(options)
    ])
