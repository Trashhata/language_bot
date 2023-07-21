from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from data_base.users import USER_BASE

from keyboards import keyboards, lesson_keyboard, main_menu, word_list

from lexicon.lexicon_en import MAIN_LEXICON, REGISTRATION, LEXICON_COMMANDS

from services import lesson_services


router: Router = Router()


# HANDLER FOR /START COMMAND
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_COMMANDS['/start'])
    # HERE WILL BE REGISTRATION


# HANDLER FOR /HELP COMMAND
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_COMMANDS['/help'])
