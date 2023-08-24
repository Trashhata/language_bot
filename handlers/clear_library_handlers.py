from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState
from lexicon.lexicon_en import ACCOUNT_SETTINGS

from keyboards.clear_library_keyboard import CANCEL_K_B
from keyboards.word_library_keyboards import LIBRARY_MAIN_K_B

from services.word_library_services import clear_library

router: Router = Router()


# handler for library clear confirmation
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       F.data == 'clear_library')
async def clear_library_confirmation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.CLEAR_LIBRARY)

    await callback.message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['CONFIRMATION'],
                                  reply_markup=CANCEL_K_B)


# handler for confirmed clear
@router.message(StateFilter(StudentState.CLEAR_LIBRARY),
                F.text == 'CLEAR LIBRARY')
async def clear_library_confirmed(message: Message, state: FSMContext):
    await clear_library(message.from_user.id)

    await state.set_state(StudentState.WORD_LIBRARY)
    await message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['SUCCESS'],
                         reply_markup=LIBRARY_MAIN_K_B)


# handler for clear cancellation
@router.callback_query(StateFilter(StudentState.CLEAR_LIBRARY),
                       F.data == 'cancel')
async def clear_library_cancellation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.WORD_LIBRARY)
    await callback.message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['INITIALIZATION'],
                                  reply_markup=LIBRARY_MAIN_K_B)
