from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

from states.states import StudentState
from keyboards.options_keyboards import options_k_b
from keyboards.lesson_keyboard import AMOUNT_SELECTION_KEYBOARD

from lexicon.lang_selection import get_phrase

from states import states
from aiogram.fsm.context import FSMContext


router: Router = Router()


# HANDLER FOR /START COMMAND
@router.message(CommandStart(), StateFilter(states.StudentState.REGISTERED))
async def process_start_command(message: Message):
    await message.answer(text=await get_phrase(message.from_user.id, 'START_MESSAGE'))


# HANDLER FOR /HELP COMMAND
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=await get_phrase(message.from_user.id, 'HELP_MESSAGE'))


# HANDLER FOR NEW WORDS LEARNING
@router.message(Command(commands=('new_lesson', 'repetition')), StateFilter(StudentState.REGISTERED))
async def process_new_lesson_command(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'LESSON_START'))

    if message.text == '/new_lesson':
        await state.update_data(lesson_type='new_lesson')
    elif message.text == '/repetition':
        await state.update_data(lesson_type='repetition')

    await state.set_state(StudentState.WORDS_AMOUNT_CHOICE)
    await message.answer(text=await get_phrase(message.from_user.id, 'AMOUNT_SELECTION'),
                         reply_markup=AMOUNT_SELECTION_KEYBOARD)


# HANDLER FOR OPTIONS
@router.message(Command(commands='settings'), StateFilter(StudentState.REGISTERED))
async def process_options_command(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'SETTINGS_DESCR'))

    await state.set_state(StudentState.IN_OPTIONS)
    await message.answer(text=await get_phrase(message.from_user.id, 'MAIN_MENU'),
                         reply_markup=await options_k_b(message.from_user.id))


# HANDLER FOR RETURNING TO THE MAIN MENU
@router.message(Command(commands='return'), StateFilter(StudentState.REGISTERED, StudentState.WORDS_AMOUNT_CHOICE,
                                                        StudentState.IN_LESSON, StudentState.LESSON_IS_OVER,
                                                        StudentState.IN_OPTIONS, StudentState.USER_INFO_MENU,
                                                        StudentState.USER_INFO_CHANGE, StudentState.WORD_LIBRARY,
                                                        StudentState.CLEAR_LIBRARY, StudentState.LANG_OPTIONS,
                                                        StudentState.ENTER_NEW_WORD, StudentState.CHANGE_NAME,
                                                        StudentState.CHANGE_AGE, StudentState.CHANGE_PHOTO,
                                                        StudentState.ENTER_NEW_WORD_TRANSLATION)
                )
async def reset_state_command(message: Message, state: FSMContext):
    await state.set_state(StudentState.REGISTERED)
    await message.answer(text=await get_phrase(message.from_user.id, 'BACK_TO_MENU'))
