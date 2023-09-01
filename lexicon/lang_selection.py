from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU

from data_base.sqlite_base import get_lang


async def get_phrase(user_id: int, key: str, reg: bool = False, reg_lang: str = 'ru') -> str | dict:
    if not reg:
        lang = await get_lang(user_id)

    else:
        lang = reg_lang

    if lang == 'ru':
        lex: dict = LEXICON_RU

    elif lang == 'en':
        lex: dict = LEXICON_EN

    try:
        return lex[key]

    except KeyError:
        return 'Error'
