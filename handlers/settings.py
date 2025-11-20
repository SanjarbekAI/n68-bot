from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from filters.admin import IsAdmin
from keyboards.inline import inline_keyboard_test

router = Router()


@router.message(F.text == '⚙️ Settings')
async def settings_handler(message: Message):
    text = "Settings is working"
    await message.answer(text=text, reply_markup=inline_keyboard_test)


@router.callback_query(F.data == 'inline_keyboard', IsAdmin())
async def settings_handler(call: CallbackQuery):
    message = call.message

    text = "Inline keyboard is working"
    await message.answer(text=text, reply_markup=inline_keyboard_test)


class FileStates(StatesGroup):
    waiting_for_file = State()


@router.message(Command('file'))
async def get_file_id(message: Message, state: FSMContext):
    text = "Enter file"
    await message.answer(text)
    await state.set_state(FileStates.waiting_for_file)


@router.message(FileStates.waiting_for_file, F.content_type == ContentType.PHOTO)
async def send_file_id(message: Message):
    with open('media/img.png', 'rb') as image_file:
        image_binary = image_file.read()

    # Create BufferedInputFile from binary data
    photo = BufferedInputFile(
        file=image_binary,
        filename='image.png')

    await message.answer_photo(photo=photo)
