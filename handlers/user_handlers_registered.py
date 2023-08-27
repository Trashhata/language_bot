from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

from states.states import StudentState
from keyboards import lesson_keyboard, options_keyboards

from lexicon.lexicon_en import MAIN_MENU_LEXICON, LESSON_LEXICON, ACCOUNT_SETTINGS

from states import states
from aiogram.fsm.context import FSMContext


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
@router.message(Command(commands=('new_lesson', 'repetition')), StateFilter(StudentState.REGISTERED))
async def process_new_lesson_command(message: Message, state: FSMContext):
    await message.answer(MAIN_MENU_LEXICON['LESSON_START'])

    if message.text == '/new_lesson':
        await state.update_data(lesson_type='new_lesson')
    elif message.text == '/repetition':
        await state.update_data(lesson_type='repetition')

    await state.set_state(StudentState.WORDS_AMOUNT_CHOICE)
    await message.answer(text=LESSON_LEXICON['AMOUNT_SELECTION'],
                         reply_markup=lesson_keyboard.AMOUNT_SELECTION_KEYBOARD)


# HANDLER FOR OPTIONS
@router.message(Command(commands='settings'), StateFilter(StudentState.REGISTERED))
async def process_options_command(message: Message, state: FSMContext):
    await message.answer(MAIN_MENU_LEXICON['SETTINGS_DESCR'])

    await state.set_state(StudentState.IN_OPTIONS)
    await message.answer(text=ACCOUNT_SETTINGS['MAIN_MENU'],
                         reply_markup=options_keyboards.MAIN_OPTIONS_MENU_KB)


# HANDLER FOR RETURN COMMAND
@router.message(Command(commands='return'), StateFilter(StudentState.REGISTERED))
async def process_return_command(message: Message, state: FSMContext):
    await state.set_state(StudentState.REGISTERED)

    await message.answer(text=MAIN_MENU_LEXICON['START_MESSAGE'])


# DEBUG STATE RESET COMMAND
@router.message(Command(commands='reset_state'))
async def reset_state_command(message: Message, state: FSMContext):
    await state.set_state(StudentState.REGISTERED)
    await message.answer(text='INFO: State was set to "Registered".')
