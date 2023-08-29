from external_services.get_random_word import Word


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
        self.__words_backup: list[Word] = [choice.right_answer for choice in words]

    @property
    def words(self):
        return self.__words

    @property
    def right_answer(self):
        return self.__right_answer

    @property
    def words_backup(self):
        return self.__words_backup

    def __call__(self, *args, **kwargs):
        try:
            next_word = next(self.words)
            self.__right_answer = next_word.right_answer.translation
            # print(next_word.right_answer.word, next_word.right_answer.translation)
            #
            # print(self.__right_answer)

            return next_word

        except StopIteration:

            return None


class User:
    def __init__(self, student_data: dict):
        self.__id: int = student_data['id']
        self.__name: str = student_data['name']
        self.__age: int = student_data['age']
        # telegram id of user photo
        self.__photo: str = student_data['photo']

        if 'words' not in student_data.keys():
            self.__words: dict[str, Word] = dict()

        else:
            self.__words: dict[str, Word] = student_data['words']

        # executed lesson
        self.__current_lesson: Lesson | None = None

    @property
    def id(self):
        return self.__id

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
    def words(self) -> dict[str, Word]:
        return self.__words

    @property
    def lesson(self):
        return self.__current_lesson

    @property
    def right_answer(self):
        return self.__current_lesson.right_answer

    @lesson.setter
    def lesson(self, lesson):
        self.__current_lesson = lesson

    def add_word(self, addable: Word):
        if not self.__words.get(addable.word):
            self.__words[addable.word] = addable
            return True
        else:
            raise WordExistError('Word already in base.')

    def get_word(self, searchable: str) -> bool:
        if not self.__words.get(searchable):
            raise WordExistError('There is not such a word in base.')

        else:
            return True

    def del_word(self, deletable: str):
        try:
            self.__words.pop(deletable)
            return True
        except KeyError:
            raise WordExistError("Word doesn't exist.")

    def learned(self, word: str, learned: bool):
        try:
            self.__words[word].learned = learned
        except KeyError:
            raise WordExistError("Word doesn't exist.")

    def sort_word_base(self):
        self.__words = {k: self.__words[k] for k in sorted(self.__words.keys(), key=str.lower)}

    def clear_library(self):
        self.__words = dict()
