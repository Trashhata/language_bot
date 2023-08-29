from data_base.sqlite_base import get_from_base, update_user_obj

from external_services.get_random_word import Word

import pprint


# yields words for each page of library keyboard
async def world_library_page(user_id: int, page_number: int = 1) -> list[Word] | bool:
    word_base: dict[str, Word] = (await get_from_base(user_id)).words
    words_amount = len(word_base)

    # pprint.pprint(word_base)
    # print(words_amount)

    if words_amount % 7 == 0:
        pages_amount = words_amount // 7

    else:
        pages_amount = (words_amount // 7) + 1

    if pages_amount < page_number:
        return []

    # creates list with each page words

    current_page = []

    for index, word in enumerate(word_base.values(), 0):
        if index in range((page_number - 1) * 7, ((page_number - 1) * 7) + 7):
            current_page.append(word)

    return current_page


# clear user word library by user id
async def clear_library(user_id: int):
    user = await get_from_base(user_id)
    user.clear_library()

    await update_user_obj(user)
