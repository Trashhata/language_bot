from aiogram import Router, F

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import (CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, Message, PhotoSize)


class StudentState(StatesGroup):
    # registration states
    NAME_SETTING = State()
    AGE_SETTING = State()
    PHOTO_SETTING = State()
    REGISTERED = State()
    # lesson states
    WORDS_AMOUNT_CHOICE = State()
    IN_LESSON = State()
    LESSON_IS_OVER = State()


storage: MemoryStorage = MemoryStorage()
