from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from services.lesson_services import get_choices


def choice_keyboard_creation(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[KeyboardButton(text=word,
                                                        one_time_keyboard=True,
                                                        resize_keyboard=True) for word in get_choices(user_id)])





