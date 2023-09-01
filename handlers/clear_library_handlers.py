from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState
from lexicon.lang_selection import get_phrase

from keyboards.clear_library_keyboard import create_cancel_cb
from keyboards.word_library_keyboards import library_settings_k_b

from services.word_library_services import clear_library

router: Router = Router()


# handler for library clear confirmation
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       F.data == 'clear_library')
async def clear_library_confirmation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.CLEAR_LIBRARY)

    await callback.message.answer(text=await get_phrase(callback.from_user.id, 'CONFIRMATION'),
                                  reply_markup=await create_cancel_cb(callback.from_user.id))


# handler for confirmed clear
@router.message(StateFilter(StudentState.CLEAR_LIBRARY),
                F.text == 'CLEAR LIBRARY')
async def clear_library_confirmed(message: Message, state: FSMContext):
    await clear_library(message.from_user.id)

    await state.set_state(StudentState.WORD_LIBRARY)

    await message.answer(text=await get_phrase(message.from_user.id,'SUCCESS'),
                         reply_markup=await library_settings_k_b(message.from_user.id))
