from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states.states import StudentState

from lexicon.lexicon_en import LESSON_LEXICON
from keyboards.lesson_keyboard import choice_keyboard_creation
from services.lesson_services import start_lesson
from data_base.users import USER_BASE, Lesson


router: Router = Router()


# lesson completion
async def end_lesson(message, state):
    print('Конец занятия')
    message.answer(text='LESSON IS OVER')


# lesson logic
async def lesson_in_progress(message: Message | CallbackQuery, state: FSMContext):
    answers = USER_BASE[message.from_user.id].lesson()
    # adds information about the current right answer

    if not answers:
        await end_lesson(message, state)

    else:
        if isinstance(message, Message):
            await message.answer(text=answers.right_answer.word, reply_markup=choice_keyboard_creation(answers))

        elif isinstance(message, CallbackQuery):
            await message.message.answer(text=answers.right_answer.word, reply_markup=choice_keyboard_creation(answers))


# amount of words chose
@router.message(StateFilter(StudentState.WORDS_AMOUNT_CHOICE),
                F.func(lambda answer: int(answer.text) in range(10, 41, 5)))
async def right_amount_selected(message: Message, state: FSMContext):
    await message.answer(LESSON_LEXICON['LESSON_STARTING'])
    await state.set_state(StudentState.IN_LESSON)

    # starts lesson
    await start_lesson(amount=int(message.text),
                       user_id=message.from_user.id,
                       repetition=False)

    # first word showing
    await lesson_in_progress(message, state)


# handler for incorrect amount selection
@router.message(StateFilter(StudentState.WORDS_AMOUNT_CHOICE))
async def incorrect_amount_selected(message: Message):
    await message.answer(text=LESSON_LEXICON['INCORRECT_AMOUNT'])


# handler for answer checking while student in lesson
@router.callback_query(StateFilter(StudentState.IN_LESSON))
async def answer_check(callback_query: CallbackQuery, state: FSMContext):
    print(callback_query.data)

    if callback_query.data == 'True':
        await callback_query.message.answer(text=LESSON_LEXICON['RIGHT_ANSWER'])

    if callback_query.data == 'False':
        r_a = USER_BASE[callback_query.from_user.id].right_answer

        await callback_query.message.answer(text=LESSON_LEXICON['INCORRECT_ANSWER'] + r_a)

    await lesson_in_progress(callback_query, state)

