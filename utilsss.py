#   LOGICAL
# methods for storage the right answers, deletes the right answer, get R.A. (or None) and get+saving numbers of DB rows
# Number of rows are recalculated every time, when bot was restarted
#  SHELVE STORAGE

import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name
from telebot import types
from random import shuffle


def count_rows():
    # Метод считает общее количество строк в БД и помещает в хранилище. Потом из этого количества будем выбирать музыку
    db = SQLighter(database_name)
    rowsnum = db.counts_rows()
    with shelve.open(shelve_name) as storage:  # with: Python сам берет на себя управление закрытием хранилища.
        storage['rows_count'] = rowsnum


def get_rows_count():
    # Получает из хранилища число строк в БД
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    # Записываем юзера в игроки и запоминаем, что он должен ответить
    # chat_id: id юзера, estimated_answer: правильный ответ (из БД)
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    # Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    # Получаем правильный ответ для текущего юзера. В случае левых символов - return None.
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def generate_markup(right_answer, wrong_answers):
    # Создаем кастомную клавиатуру для выбора ответа
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    # Склеиваем правильный ответ с неправильными (в одну строку)
    all_answers = '{},{}'.format(right_answer, wrong_answers)

    # Создаем массив и записываем в него все элементы (через запятую)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)

    # Перемешиваем все элементы
    shuffle(list_items)

    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)

    return markup
