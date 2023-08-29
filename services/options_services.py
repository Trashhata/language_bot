from data_base.users import User
from data_base.sqlite_base import get_from_base, update_user_obj
from lexicon.lang_selection import get_phrase
from states.states import StudentState
from keyboards.options_keyboards import info_settings_k_b

from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.context import FSMContext


# returns string of user info and photo
async def show_profile(user_id: int) -> tuple[str, str]:
    user: User = await get_from_base(user_id)

    return f'Name: {user.name}\nAge: {user.age}\n', user.photo


# answer users messages with user profile card
async def answer_with_profile_info(message: Message | CallbackQuery):

    id_ = message.from_user.id

    if isinstance(message, CallbackQuery):
        message = message.message

    text, photo_url = await show_profile(id_)
    text_2 = text + '\n' + await get_phrase(id_, 'INFO_EDIT_INITIALIZATION')

    if photo_url is None:
        await message.answer(text=text_2, reply_markup=await info_settings_k_b(id_))
    else:
        await message.answer_photo(photo=photo_url, caption=text_2,
                                   reply_markup=await info_settings_k_b(id_))


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
    await message.answer(text=await get_phrase(message.from_user.id, 'EDITING_SUCCESS'))

    await state.set_state(StudentState.USER_INFO_MENU)
    await answer_with_profile_info(message)
