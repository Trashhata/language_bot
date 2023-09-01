from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from lexicon.lang_selection import get_phrase
from states.states import StudentState
from keyboards.options_keyboards import language_change_k_b, LanguageCustomCallback, options_k_b
from data_base.sqlite_base import update_lang

router: Router = Router()


@router.callback_query(StateFilter(StudentState.IN_OPTIONS), F.data == 'language')
async def change_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.LANG_OPTIONS)

    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'LANGUAGE_CHOICE'),
                                  reply_markup=await language_change_k_b(callback.from_user.id))


@router.callback_query(StateFilter(StudentState.LANG_OPTIONS),
                       LanguageCustomCallback.filter(F.flag == 'lang'))
async def language_switch(callback: CallbackQuery, callback_data: LanguageCustomCallback, state: FSMContext):
    id_ = callback.from_user.id

    try:
        await update_lang(id_, callback_data.lang)
        await callback.message.answer(await get_phrase(id_, 'LANGUAGE_CHANGED'))

        await state.set_state(StudentState.IN_OPTIONS)
        await callback.message.answer(text=await get_phrase(id_, 'SETTINGS_DESCR'))

        await callback.message.answer(text=await get_phrase(id_, 'MAIN_MENU'),
                                      reply_markup=await options_k_b(id_))

    except Exception:
        await callback.message.answer(await get_phrase(id_, 'LANGUAGE_NOT_CHANGED'))
