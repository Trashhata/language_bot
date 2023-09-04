from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState

from keyboards.lesson_keyboard import AmountCallback, AMOUNT_SELECTION_KEYBOARD
from lexicon.lang_selection import get_phrase
from services.lesson_services import start_lesson, lesson_in_progress, break_the_repetition_lesson
from data_base.sqlite_base import get_from_base


router: Router = Router()


# number of words chose
@router.callback_query(StateFilter(StudentState.WORDS_AMOUNT_CHOICE),
                       AmountCallback.filter(F.flag == 'amount'))
async def right_amount_selected(callback_query: CallbackQuery, callback_data: AmountCallback, state: FSMContext):
    await callback_query.answer(text=await get_phrase(callback_query.from_user.id, 'LESSON_STARTING'))
    await state.set_state(StudentState.IN_LESSON)

    repetition: bool = False if (await state.get_data())['lesson_type'] == 'new_lesson' else True

    # starts lesson
    try:
        await start_lesson(amount=int(callback_data.amount),
                           user_id=callback_query.from_user.id,
                           repetition=repetition)
    # except ValueError as error:
    #     print(f'Ебучая ошибка\n{error}')
    #
    #     await break_the_repetition_lesson(callback_query, state)


    try:
        # first word showing
        await lesson_in_progress(callback_query, state)

    except Exception:
        await callback_query.answer(text=await get_phrase(callback_query.from_user.id, 'CRASH'))
        await state.set_state(StudentState.REGISTERED)
        raise


# handler for incorrect amount selection
@router.message(StateFilter(StudentState.WORDS_AMOUNT_CHOICE))
async def incorrect_amount_selected(message: Message):
    await message.answer(text=await get_phrase(message.from_user.id, 'INCORRECT_AMOUNT'))


# handler for answer checking while student in lesson
@router.callback_query(StateFilter(StudentState.IN_LESSON))
async def answer_check(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'True':
        await callback_query.message.answer(text=await get_phrase(callback_query.from_user.id, 'RIGHT_ANSWER'))

    if callback_query.data == 'False':
        r_a = (await get_from_base(callback_query.from_user.id)).right_answer

        await callback_query.message.answer(text=(await get_phrase(callback_query.from_user.id,
                                                                   'INCORRECT_ANSWER') + r_a))

    await lesson_in_progress(callback_query, state)


@router.callback_query(StateFilter(StudentState.LESSON_IS_OVER), F.data == 'repeat')
async def restart_lesson(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text=await get_phrase(callback_query.from_user.id, 'LESSON_START'))

    await state.set_state(StudentState.WORDS_AMOUNT_CHOICE)
    await callback_query.message.answer(text=await get_phrase(callback_query.from_user.id, 'AMOUNT_SELECTION'),
                                        reply_markup=AMOUNT_SELECTION_KEYBOARD)


@router.callback_query(StateFilter(StudentState.LESSON_IS_OVER), F.data == 'finish')
async def finish_lesson(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text=await get_phrase(callback_query.from_user.id, 'BACK_TO_MENU'))
    await state.set_state(StudentState.REGISTERED)
