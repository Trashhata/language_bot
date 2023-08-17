from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis


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


storage: RedisStorage = RedisStorage(redis=redis.Redis(host='localhost',
                                                       port=6379,
                                                       decode_responses=True)
                                     )
