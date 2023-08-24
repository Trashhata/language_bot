from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.states import StudentState
from lexicon.lexicon_en import ACCOUNT_SETTINGS
from services.new_word_add_services import check_if_exists, push_new_word

from keyboards.clear_library_keyboard import CANCEL_K_B
from keyboards.word_library_keyboards import LIBRARY_MAIN_K_B


router: Router = Router()


# handler for a new word enter
@router.callback_query(StateFilter(StudentState.WORD_LIBRARY),
                       F.data == 'new_word')
async def add_new_word(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.ENTER_NEW_WORD)

    await callback.message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['WORD'],
                                  reply_markup=CANCEL_K_B)


# handler for a new word translation enter
@router.message(StateFilter(StudentState.ENTER_NEW_WORD),
                F.func(lambda message: message.text.isalpha()))
async def add_new_word_translation(message: Message, state: FSMContext):
    # check if word already in library
    check: bool = await check_if_exists(user_id=message.from_user.id, word=message.text)
    print(check)

    if check is False:
        await state.set_state(StudentState.ENTER_NEW_WORD_TRANSLATION)
        await state.update_data(word=message.text)

        await message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['TRANSLATION'],
                             reply_markup=CANCEL_K_B)

    # if in library, returns user back in the library menu
    else:
        await state.set_state(StudentState.WORD_LIBRARY)

        await message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['WORD_EXIST'],
                             reply_markup=LIBRARY_MAIN_K_B)


# handler for new word add confirmation
@router.message(StateFilter(StudentState.ENTER_NEW_WORD_TRANSLATION),
                F.func(lambda message: message.text.isalpha()))
async def add_new_word_confirmation(message: Message, state: FSMContext):
    # writes new word into base
    await push_new_word(user_id=message.from_user.id,
                        word=(await state.get_data())['word'],
                        translation=message.text)

    # returns user back in the library menu
    await state.set_state(StudentState.WORD_LIBRARY)
    await message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['WORD_ADDED'],
                         reply_markup=LIBRARY_MAIN_K_B)


# handler for new word add cancellation
@router.callback_query(StateFilter(StudentState.ENTER_NEW_WORD, StudentState.ENTER_NEW_WORD_TRANSLATION),
                       F.data == 'cancel')
async def new_word_add_cancellation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StudentState.WORD_LIBRARY)
    await callback.message.answer(text=ACCOUNT_SETTINGS['WORD_LIBRARY']['INITIALIZATION'],
                                  reply_markup=LIBRARY_MAIN_K_B)
