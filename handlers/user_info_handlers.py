from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState
from lexicon.lang_selection import get_phrase

from keyboards.options_keyboards import UserInfoChangeCallback, options_k_b
from keyboards.word_library_keyboards import library_settings_k_b

from services.options_services import change_info, answer_with_profile_info
from filters.user_info_filters import age_filter


router: Router = Router()


# entrance to info settings
@router.callback_query(StateFilter(StudentState.IN_OPTIONS),
                       F.data == 'user_info')
async def user_info_menu_selected(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.USER_INFO_MENU)

    await answer_with_profile_info(callback)


# entrance to user library
@router.callback_query(StateFilter(StudentState.IN_OPTIONS),
                       F.data == 'library')
async def word_library_selected(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.WORD_LIBRARY)

    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'LIBRARY_EDIT_INITIALIZATION'),
                                  reply_markup=await library_settings_k_b(callback.from_user.id))


# handler for clear cancellation or exit from library editing
@router.callback_query(StateFilter(StudentState.CLEAR_LIBRARY,
                                   StudentState.WORD_LIBRARY),
                       F.data == 'cancel')
async def clear_or_edit_library_cancellation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.WORD_LIBRARY)
    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'LIBRARY_EDIT_INITIALIZATION'),
                                  reply_markup=await library_settings_k_b(callback.from_user.id))


# handler for user info change
@router.callback_query(StateFilter(StudentState.USER_INFO_MENU),
                       UserInfoChangeCallback.filter(F.flag == 'user_info_change'))
async def user_info_change(callback: CallbackQuery,
                           callback_data: UserInfoChangeCallback,
                           state: FSMContext):

    # the dict of tuples with states and texts for answer
    state_and_answer_param: dict[str, tuple[State, str]] = {
        'name': (StudentState.CHANGE_NAME, await get_phrase(callback.from_user.id, 'EDIT_NAME')),
        'age': (StudentState.CHANGE_AGE, await get_phrase(callback.from_user.id, 'EDIT_AGE')),
        'photo': (StudentState.CHANGE_PHOTO, await get_phrase(callback.from_user.id, 'EDIT_AVATAR')),
    }

    await state.set_state(state_and_answer_param[callback_data.option][0])
    await state.update_data(param=callback_data.option)

    await callback.message.answer(text=state_and_answer_param[callback_data.option][1])


# handler for back button
@router.callback_query(StateFilter(StudentState.USER_INFO_MENU),
                       F.data == 'back')
async def return_to_setting_menu(callback: CallbackQuery, state: FSMContext):
    id_ = callback.from_user.id

    await callback.message.answer(text=await get_phrase(id_, 'SETTINGS_DESCR'))

    await state.set_state(StudentState.IN_OPTIONS)
    await callback.message.answer(text=await get_phrase(id_, 'MAIN_MENU'),
                                  reply_markup=await options_k_b(id_))


# handler for name editing
@router.message(StateFilter(StudentState.CHANGE_NAME), F.text.isalpha())
async def name_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_NAME))
async def name_edit_incorrect(message: Message):
    await message.answer(await get_phrase(message.from_user.id, 'INCORRECT_NAME'))


# handler for age editing
@router.message(StateFilter(StudentState.CHANGE_AGE),
                age_filter)
async def age_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_NAME))
async def age_edit_incorrect(message: Message):
    await message.answer(await get_phrase(message.from_user.id, 'INCORRECT_AGE'))


# handler for photo editing
@router.message(StateFilter(StudentState.CHANGE_PHOTO), F.photo)
async def photo_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_PHOTO))
async def age_edit_incorrect(message: Message):
    await message.answer(await get_phrase(message.from_user.id, 'INCORRECT_DATA'))
