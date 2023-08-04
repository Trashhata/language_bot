from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

import keyboards.keyboards
from states.states import StudentState

from lexicon.lexicon_en import REGISTRATION, LEXICON_COMMANDS, MAIN_MENU_LEXICON
from data_base.users import USER_BASE, User


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command_registration(message: Message, state: FSMContext):
    if USER_BASE.get(message.from_user.id):
        await message.answer(MAIN_MENU_LEXICON['START_MESSAGE'])
        await state.set_state(StudentState.REGISTERED)

    else:
        await message.answer(text=REGISTRATION['INITIALIZATION'])
        await state.set_state(StudentState.NAME_SETTING)


@router.message(StateFilter(StudentState.NAME_SETTING), F.text.isalpha())
async def correct_name_enter(message: Message, state: FSMContext):
    await message.answer(text=REGISTRATION['AGE_ENTER'])

    await state.update_data(name=message.text)
    await state.set_state(StudentState.AGE_SETTING)


@router.message(StateFilter(StudentState.NAME_SETTING))
async def incorrect_name_enter(message: Message):
    await message.answer(text=REGISTRATION['INCORRECT_NAME'])


@router.message(StateFilter(StudentState.AGE_SETTING),
                lambda answer: answer.text.isdigit() and 5 <= int(answer.text) <= 110)
async def correct_age_enter(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(StudentState.PHOTO_SETTING)

    await message.answer(text=REGISTRATION['AVATAR_SELECTION'],
                         reply_markup=keyboards.keyboards.SKIP_KEYBOARD)


@router.message(StateFilter(StudentState.AGE_SETTING))
async def incorrect_age_enter(message: Message):
    await message.answer(text=REGISTRATION['INCORRECT_AGE'])


@router.message(StateFilter(StudentState.PHOTO_SETTING), F.photo)
async def correct_photo_upload(message: Message, state: FSMContext):
    await message.answer(text=REGISTRATION['REGISTRATION_FINISHED'])

    await state.update_data(photo=message.photo)
    await state.set_state(StudentState.REGISTERED)

    USER_BASE[message.from_user.id] = User(await state.get_data())


@router.callback_query(StateFilter(StudentState.PHOTO_SETTING), F.data == 'Skip.')
async def skip_photo_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text=REGISTRATION['REGISTRATION_FINISHED'])

    await state.update_data(photo=None)
    await state.set_state(StudentState.REGISTERED)

    USER_BASE[callback_query.from_user.id] = User(await state.get_data())


@router.message(StateFilter(StudentState.PHOTO_SETTING))
async def incorrect_age_enter(message: Message):
    await message.answer(text=REGISTRATION['INCORRECT_DATA'])
