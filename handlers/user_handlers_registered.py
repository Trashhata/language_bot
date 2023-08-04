from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from states.states import StudentState

from data_base.users import USER_BASE

from keyboards import keyboards, lesson_keyboard, main_menu, word_list

from lexicon.lexicon_en import MAIN_MENU_LEXICON, LESSON_LEXICON

from states import states
from services import lesson_services
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


router: Router = Router()


# HANDLER FOR /START COMMAND
@router.message(CommandStart(), StateFilter(states.StudentState.REGISTERED))
async def process_start_command(message: Message):
    await message.answer(MAIN_MENU_LEXICON['START_MESSAGE'])


# HANDLER FOR /HELP COMMAND
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(MAIN_MENU_LEXICON['HELP_MESSAGE'])


# HANDLER FOR NEW WORDS LEARNING
@router.message(Command(commands='new_lesson'), StateFilter(StudentState.REGISTERED))
async def process_new_lesson_command(message: Message, state: FSMContext):
    await message.answer(MAIN_MENU_LEXICON['LESSON_START'])

    await state.set_state(StudentState.WORDS_AMOUNT_CHOICE)
    await message.answer(text=LESSON_LEXICON['AMOUNT_SELECTION'],
                         reply_markup=lesson_keyboard.AMOUNT_SELECTION_KEYBOARD)


# HANDLER FOR REPETITION
@router.message(Command(commands='repetition'), StateFilter(StudentState.REGISTERED))
async def process_repetition_command(message: Message):
    await message.answer(MAIN_MENU_LEXICON['LESSON_START'])


# HANDLER FOR OPTIONS
@router.message(Command(commands='settings'), StateFilter(StudentState.REGISTERED))
async def process_options_command(message: Message):
    await message.answer(MAIN_MENU_LEXICON['SETTINGS_DESCR'])


