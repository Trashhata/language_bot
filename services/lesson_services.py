from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data_base.users import USER_BASE
from external_services.words_generator import get_new_word
from random import sample


def get_choices(user_id: int) -> iter:
    pass


def new_words_generation(amount: int):
    yield from (get_new_word() for _ in range(amount))


def repetition_words(user_id: int, amount: int):
    yield from (sample([i for i in USER_BASE[user_id].words if not i[1]['learned']], amount))