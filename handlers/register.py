from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.default import phone_number, user_main_menu
from keyboards.inline import languages
from states.register import RegisterState
from utils.db_commands.user import add_user, get_user

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
    if await get_user(chat_id=message.chat.id):
        text = "Welcome 😊"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = "Iltimos tilni tanlang\nPlease select the language."
        await message.answer(text=text, reply_markup=languages)
        await state.set_state(RegisterState.language)


@router.callback_query(RegisterState.language)
async def language_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(language=call.data)
    if call.data == "en":
        text = "Please enter your full name"
    else:
        text = "Iltimos to'liq ismingizni kiriting"
    await call.message.answer(text=text)
    await state.set_state(RegisterState.full_name)


@router.message(RegisterState.full_name)
async def full_name_handler(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get('language')
    if lang == "en":
        text = "Please enter your phone number"
    else:
        text = "Iltimos telefon raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone_number)
    await state.set_state(RegisterState.phone_number)


@router.message(RegisterState.phone_number, F.content_type == ContentType.CONTACT)
async def phone_number_handler(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    lang = data.get('language')
    if lang == "en":
        text = "Please enter your age"
    else:
        text = "Iltimos yoshingizni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterState.age)


@router.message(RegisterState.phone_number)
async def phone_number_handler(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    lang = data.get('language')
    if lang == "en":
        text = "Please enter your age"
    else:
        text = "Iltimos yoshingizni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterState.age)


@router.message(RegisterState.age)
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text, chat_id=message.chat.id, created_at=message.date)
    data = await state.get_data()
    lang = data.get('language')

    new_user = await add_user(data=data)
    if new_user:
        if lang == "en":
            text = "Successfully registered ✅"
        else:
            text = "Muvaffaqqiyatli ro'yxatdan o'tdingiz ✅"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        if lang == "en":
            text = "Not registered"
        else:
            text = "Botda muommo mavjud biz bilan bog'laning"
        await message.answer(text=text)
    await state.clear()
