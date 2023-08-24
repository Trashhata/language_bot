from data_base.sqlite_base import get_from_base, update_user_obj
from data_base.users import User, WordExistError

from external_services.get_random_word import Word


# checks if word already in base
async def check_if_exists(user_id: int, word: str) -> bool:
    user: User = await get_from_base(user_id)
    try:
        return user.get_word(word)

    except WordExistError:
        return False


# adds new word into the base
async def push_new_word(user_id: int, word: str, translation: str):
    new_word: Word = Word(word, translation)

    user: User = await get_from_base(user_id)

    try:
        user.add_word(new_word)
        user.sort_word_base()

    except WordExistError as error:
        print(error)

    await update_user_obj(user)
