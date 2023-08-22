from data_base.users import User
from data_base.sqlite_base import get_from_base, update_user_obj
from lexicon.lexicon_en import ACCOUNT_SETTINGS
from states.states import StudentState
from keyboards.options_keyboards import USER_INFO_K_b

from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.context import FSMContext


# returns string of user info and photo
async def show_profile(user_id: int) -> tuple[str, str]:
    user: User = await get_from_base(user_id)

    return f'Name: {user.name}\nAge: {user.age}\n', user.photo


# answer users message with users profile card
async def answer_with_profile_info(message: Message | CallbackQuery):

    id_ = message.from_user.id

    if isinstance(message, CallbackQuery):
        message = message.message

    text, photo_url = await show_profile(id_)
    text_2 = text + '\n' + ACCOUNT_SETTINGS['USER_INFORMATION']['INITIALIZATION']

    if photo_url is None:
        await message.answer(text=text_2, reply_markup=USER_INFO_K_b)
    else:
        await message.answer_photo(photo=photo_url, caption=text_2, reply_markup=USER_INFO_K_b)


# changes user info by one of 3 params: name, age, photo
async def change_info(message: Message, state: FSMContext, param: str):
    user: User = await get_from_base(message.from_user.id)

    if param == 'name':
        user.name = message.text

    elif param == 'age':
        user.age = int(message.text)

    elif param == 'photo':
        photo: PhotoSize = message.photo[0]

        user.photo = photo.file_id

    await update_user_obj(user)
    await message.answer(text=ACCOUNT_SETTINGS['USER_INFORMATION']['EDITING']['EDITING_SUCCESS'])

    await state.set_state(StudentState.USER_INFO_MENU)
    await answer_with_profile_info(message)
