from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="UZ 🇺🇿", callback_data="uz"),
            InlineKeyboardButton(text="EN 🇺🇸", callback_data="en")
        ]
    ]
)

inline_keyboard_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Test", callback_data="inline_keyboard")
        ]
    ]
)
