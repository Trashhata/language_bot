from dataclasses import dataclass
from dictionaries.get_dictionary import get_dictionary

import csv
from random import sample


@dataclass
class Word:
    word: str
    translation: str


# origin - origin language, res - result language
def get_new_words(amount: int, origin: str = 'en', res: str = 'ru') -> list[Word]:
    # csv file with dictionary
    dictionary = get_dictionary(language=f'{origin}-{res}')

    reader = csv.reader(dictionary)
    res = sample(list(reader), amount)
    dictionary.close()

    return [Word(*i) for i in res]
