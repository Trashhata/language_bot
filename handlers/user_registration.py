from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import keyboards.keyboards
from keyboards.keyboards import LanguageCustomCallback, language_select_k_b

from states.states import StudentState
from lexicon.lang_selection import get_phrase
from data_base.sqlite_base import write_into_base, get_from_base
from filters.user_info_filters import age_filter

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command_registration(message: Message, state: FSMContext):
    try:
        await get_from_base(message.from_user.id)

    # if a user isn't in base
    except Exception:
        await message.answer(text=await get_phrase(message.from_user.id, 'REGISTRATION_INITIALIZATION',
                                                   reg=True, reg_lang='ru'),
                             reply_markup=await language_select_k_b(message.from_user.id))

        await state.update_data(id=message.from_user.id)
        await state.set_state(StudentState.LANG_SETTING)

    else:
        await state.set_state(StudentState.REGISTERED)
        await message.answer(text=await get_phrase(message.from_user.id, 'START_MESSAGE'))


@router.callback_query(StateFilter(StudentState.LANG_SETTING),
                       LanguageCustomCallback.filter(F.data == 'language'))
async def lang_selected(callback: CallbackQuery, callback_data: LanguageCustomCallback, state: FSMContext):
    await state.update_data(lang=callback_data.lang)
    await state.set_state(StudentState.NAME_SETTING)

    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'NAME_SELECTION',
                                                        reg=True, reg_lang=(await state.get_data())['lang']))

    await state.set_state(StudentState.NAME_SETTING)


@router.message(StateFilter(StudentState.NAME_SETTING), F.text.isalpha())
async def correct_name_enter(message: Message, state: FSMContext):

    await message.answer(text=await get_phrase(message.from_user.id, 'AGE_ENTER'),
                         reg=True, reg_lang=(await state.get_data())['lang'])

    await state.update_data(name=message.text)
    await state.set_state(StudentState.AGE_SETTING)


@router.message(StateFilter(StudentState.NAME_SETTING))
async def incorrect_name_enter(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'INCORRECT_NAME'),
                         reg=True, reg_lang=(await state.get_data())['lang'])


@router.message(StateFilter(StudentState.AGE_SETTING),
                age_filter)
async def correct_age_enter(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(StudentState.PHOTO_SETTING)

    await message.answer(text=await get_phrase(message.from_user.id, 'AVATAR_SELECTION',
                                               reg=True, reg_lang=(await state.get_data())['lang']),
                         reply_markup=await keyboards.keyboards.skip_k_b(message.from_user.id))


@router.message(StateFilter(StudentState.AGE_SETTING))
async def incorrect_age_enter(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'INCORRECT_AGE'),
                         reg=True, reg_lang=(await state.get_data())['lang'])


@router.message(StateFilter(StudentState.PHOTO_SETTING), F.photo)
async def correct_photo_upload(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'REGISTRATION_FINISHED',
                                               reg=True, reg_lang=(await state.get_data())['lang']))

    photo: PhotoSize = message.photo[0]

    await state.update_data(photo=photo.file_id)
    await state.set_state(StudentState.REGISTERED)

    user_id, data = message.from_user.id, await state.get_data()

    # adds user into current session base and permanent base
    await write_into_base(data)


@router.callback_query(StateFilter(StudentState.PHOTO_SETTING), F.data == 'Skip.')
async def skip_photo_selection(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text=await get_phrase(callback_query.from_user.id, 'REGISTRATION_FINISHED'),
                                        reg=True, reg_lang=(await state.get_data())['lang'])

    await state.update_data(photo=None)
    await state.set_state(StudentState.REGISTERED)

    await write_into_base(await state.get_data())


@router.message(StateFilter(StudentState.PHOTO_SETTING))
async def incorrect_age_enter(message: Message, state: FSMContext):
    await message.answer(text=await get_phrase(message.from_user.id, 'INCORRECT_DATA'),
                         reg=True, reg_lang=(await state.get_data())['lang'])
