from external_services.get_info import get_info
from typing import Generator


class WordExistError(Exception):
    pass


"""
Words is a list of Choices.
Each call of a class object remove one word from it.
"""


class Lesson:
    def __init__(self, words: list):
        self.__words = iter(words)
        self.__right_answer = None

    @property
    def words(self):
        return self.__words

    @property
    def right_answer(self):
        return self.__right_answer

    def __call__(self, *args, **kwargs):
        try:
            next_word = next(self.words)
            self.__right_answer = next_word.right_answer.translation
            print(next_word.right_answer.word, next_word.right_answer.translation)

            print(self.__right_answer)

            return next_word

        except StopIteration:

            return None


class User:
    def __init__(self, student_data: dict):
        self.__name = student_data['name']
        self.__age = student_data['age']
        self.__photo = student_data['photo']
        self.__words: dict[str, dict] = dict()
        # executed lesson
        self.__current_lesson: Lesson | None = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, new_age):
        self.__age = new_age

    @property
    def photo(self):
        return self.__photo

    @photo.setter
    def photo(self, new_photo):
        self.__photo = new_photo

    @property
    def words(self) -> iter:
        return iter((word, info) for word, info in sorted(self.__words.items()))

    @property
    def lesson(self):
        return self.__current_lesson

    @property
    def right_answer(self):
        return self.__current_lesson.right_answer

    @lesson.setter
    def lesson(self, lesson):
        self.__current_lesson = lesson

    def add_word(self, addable: str):
        if not self.__words.get(addable):
            self.__words[addable] = get_info()
            return True
        else:
            raise WordExistError('Word already in base.')

    def del_word(self, delitable: str):
        try:
            self.__words.pop(delitable)
            return True
        except KeyError:
            raise WordExistError("Word doesn't exist.")

    def learned(self, word: str, learned: bool):
        try:
            self.__words[word]['learned'] = learned
        except KeyError:
            raise WordExistError("Word doesn't exist.")


USER_BASE: dict[int, User] = {}
