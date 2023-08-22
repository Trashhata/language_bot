from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState
from lexicon.lexicon_en import ACCOUNT_SETTINGS, REGISTRATION
from keyboards.options_keyboards import LIBRARY_MAIN_K_B, UserInfoChangeCallback
from services.options_services import change_info, answer_with_profile_info
from filters.user_info_filters import age_filter
from handlers.user_handlers_registered import process_options_command

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

    await callback.message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['INITIALIZATION'],
                                  reply_markup=LIBRARY_MAIN_K_B)


# handler for user info change
@router.callback_query(StateFilter(StudentState.USER_INFO_MENU),
                       UserInfoChangeCallback.filter(F.flag == 'user_info_change'))
async def user_info_change(callback: CallbackQuery,
                           callback_data: UserInfoChangeCallback,
                           state: FSMContext):

    # the dict of tuples with states and texts for answer
    state_and_answer_param: dict[str, tuple[State, str]] = {
        'name': (StudentState.CHANGE_NAME, ACCOUNT_SETTINGS['USER_INFORMATION']['EDITING']['EDIT_NAME']),
        'age': (StudentState.CHANGE_AGE, ACCOUNT_SETTINGS['USER_INFORMATION']['EDITING']['EDIT_AGE']),
        'photo': (StudentState.CHANGE_PHOTO, ACCOUNT_SETTINGS['USER_INFORMATION']['EDITING']['EDIT_AVATAR'])
    }

    await state.set_state(state_and_answer_param[callback_data.option][0])
    await state.update_data(param=callback_data.option)

    await callback.message.answer(text=state_and_answer_param[callback_data.option][1])


# handler for back button
@router.callback_query(StateFilter(StudentState.USER_INFO_MENU),
                       F.data == 'back')
async def return_to_setting_menu(callback: CallbackQuery, state: FSMContext):
    await process_options_command(callback.message, state)


# handler for name editing
@router.message(StateFilter(StudentState.CHANGE_NAME), F.text.isalpha())
async def name_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_NAME))
async def name_edit_incorrect(message: Message):
    await message.answer(REGISTRATION['INCORRECT_NAME'])


# handler for age editing
@router.message(StateFilter(StudentState.CHANGE_AGE),
                age_filter)
async def age_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_NAME))
async def age_edit_incorrect(message: Message):
    await message.answer(REGISTRATION['INCORRECT_AGE'])


# handler for photo editing
@router.message(StateFilter(StudentState.CHANGE_PHOTO), F.photo)
async def photo_edit_correct(message: Message, state: FSMContext):
    data: dict = await state.get_data()

    await change_info(message, state, data['param'])


@router.message(StateFilter(StudentState.CHANGE_PHOTO))
async def age_edit_incorrect(message: Message):
    await message.answer(REGISTRATION['INCORRECT_DATA'])

