from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Sharing/Ulashish", request_contact=True)
    ]], resize_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Profile"),
            KeyboardButton(text="⚙️ Settings"),
        ]
    ], resize_keyboard=True
)
