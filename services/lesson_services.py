from data_base.users import Lesson, get_from_base, write_into_base, update_user_obj
from external_services.get_random_word import get_new_words, Word
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
    return sample([i for i in (await get_from_base(user_id)).words if not i[1]['learned']], amount)


# lesson logic. Generates words for lesson.
async def start_lesson(amount: int, user_id: int, repetition: bool = False):
    if repetition:
        lesson_words: list[Word] = await repetition_words(user_id, amount)
    else:
        lesson_words: list[Word] = get_new_words(amount)

    print(*(i.word for i in lesson_words))

    user = await get_from_base(user_id)
    user.lesson = Lesson([get_choices(word, sample([i for i in lesson_words if i.word != word.word], 3)) for word in lesson_words])
    await update_user_obj(user)
