from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from data_base.sqlite_base import get_from_base, update_user_obj
from data_base.users import User, WordExistError

from states.states import StudentState
from keyboards.word_library_keyboards import (generate_library_page, CustomCallbackTurnPage,
                                              CustomCallbackWordLearned, CustomCallbackWordDelete)
from lexicon.lang_selection import get_phrase

router: Router = Router()


# handler for library edit
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       F.data == 'edit_library')
async def edit_library_func(callback: CallbackQuery):
    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'DESCR'),
                                  reply_markup=await generate_library_page(callback.from_user.id, page=1))


# handler for turning over to next page
@router.callback_query(StateFilter(StudentState),
                       CustomCallbackTurnPage.filter(F.option == 'turn_page'))
async def next_page(callback: CallbackQuery, callback_data: CustomCallbackTurnPage):
    if callback_data.page_num not in ('first', 'last'):
        try:
            markup = await generate_library_page(callback.from_user.id,
                                                 page=int(callback_data.page_num))
        except TypeError:
            markup = await generate_library_page(callback.from_user.id,
                                                 page=int(callback_data.page_num) - 1)

        await callback.message.edit_reply_markup(reply_markup=markup)

    else:
        await callback.answer(text=f'{callback_data.page_num.capitalize()} page.')


# handler for marking as learned
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       CustomCallbackWordLearned.filter(F.data == 'learned_mark'))
async def mark_word_as_learned_or_not_learned(callback: CallbackQuery, callback_data: CustomCallbackWordLearned):
    word: str = callback_data.word
    user_id: int = callback.from_user.id

    user: User = await get_from_base(user_id)

    # marks word and write the result into base
    try:
        user.learned(word=word, learned=callback_data.option)
        await update_user_obj(user)

    except WordExistError as error:
        print(error)

    await callback.message.edit_reply_markup(reply_markup=await generate_library_page(user_id=user_id,
                                                                                      page=callback_data.current_page))


# handler for word delete
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       CustomCallbackWordDelete.filter(F.option == 'delete'))
async def delete_word_from_library(callback: CallbackQuery, callback_data: CustomCallbackWordDelete):
    word: str = callback_data.word
    user_id: int = callback.from_user.id

    user: User = await get_from_base(user_id)

    try:
        user.del_word(deletable=word)
        await update_user_obj(user)

    except WordExistError as error:
        print(error)

    await callback.message.edit_reply_markup(reply_markup=await generate_library_page(user_id=user_id,
                                                                                      page=callback_data.current_page))
