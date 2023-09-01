from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis


class StudentState(StatesGroup):
    # registration states
    LANG_SETTING = State()
    NAME_SETTING = State()
    AGE_SETTING = State()
    PHOTO_SETTING = State()
    REGISTERED = State()
    # lesson states
    WORDS_AMOUNT_CHOICE = State()
    IN_LESSON = State()
    LESSON_IS_OVER = State()
    # options menu states
    IN_OPTIONS = State()
    USER_INFO_MENU = State()
    USER_INFO_CHANGE = State()
    WORD_LIBRARY = State()
    CLEAR_LIBRARY = State()
    LANG_OPTIONS = State()
    # word add states
    ENTER_NEW_WORD = State()
    ENTER_NEW_WORD_TRANSLATION = State()
    # user info change states
    CHANGE_NAME = State()
    CHANGE_AGE = State()
    CHANGE_PHOTO = State()


storage: RedisStorage = RedisStorage(redis=redis.Redis(host='localhost'))
