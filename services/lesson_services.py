from data_base.users import Lesson, WordExistError
from data_base.sqlite_base import get_from_base, update_user_obj
from external_services.get_random_word import get_new_words, Word
from keyboards.lesson_keyboard import choice_keyboard_creation, repeat_lesson_or_not
from states.states import StudentState
from lexicon.lang_selection import get_phrase

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from random import sample
from dataclasses import dataclass


# answer choices for lesson keyboard
@dataclass
class Choices:
    right_answer: Word
    other_answers: list[Word]


# generates 4 choices for current word: 3 incorrect and 1 correct
def get_choices(right_answer: Word, collection: list) -> Choices:
    return Choices(right_answer, sample(collection, 3))


# takes words from user dictionary
async def repetition_words(user_id: int, amount: int) -> list:
    words: dict = (await get_from_base(user_id)).words

    return sample([i for i in words.values() if not i.learned], amount)


# lesson logic. Generates words for lesson.
async def start_lesson(amount: int, user_id: int, repetition: bool = False):
    if repetition:
        lesson_words: list[Word] = await repetition_words(user_id, amount)
    else:
        lesson_words: list[Word] = get_new_words(amount)

    user = await get_from_base(user_id)
    user.lesson = Lesson([get_choices(word,
                                      sample([i for i in lesson_words if i.word != word.word],
                                             3)) for word in lesson_words])
    await update_user_obj(user)


# lesson logic
async def lesson_in_progress(message: Message | CallbackQuery, state: FSMContext):
    user = await get_from_base(message.from_user.id)
    answers = user.lesson()

    await update_user_obj(user)

    if not answers:
        await end_lesson(message, state)

    else:
        if isinstance(message, Message):
            await message.answer(text=answers.right_answer.word, reply_markup=choice_keyboard_creation(answers))

        elif isinstance(message, CallbackQuery):
            await message.message.answer(text=answers.right_answer.word, reply_markup=choice_keyboard_creation(answers))


# lesson completion
async def end_lesson(message: CallbackQuery, state: FSMContext):
    # keyboard for lesson repeat
    await message.message.answer(text=await get_phrase(message.from_user.id, 'LESSON_IS_OVER'),
                                 reply_markup=await repeat_lesson_or_not(message.from_user.id))
    await state.set_state(StudentState.LESSON_IS_OVER)

    # adds new words in base if not repetition
    if (await state.get_data())['lesson_type'] == 'new_lesson':
        user = await get_from_base(message.from_user.id)

        # adds words into user dictionary
        for w in user.lesson.words_backup:
            try:
                user.add_word(w)

            except WordExistError as error:
                print(error)
                continue

        user.sort_word_base()

        # writes updated user object into base
        await update_user_obj(user)
