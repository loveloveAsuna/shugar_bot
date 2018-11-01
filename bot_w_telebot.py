
import config
import telebot
import os
import time
import random
import re
from telebot import types
from SQLighter import SQLighter
import utilsss


bot = telebot.TeleBot(config.token)
pattern = re.compile(r'news', re.MULTILINE)


def handle_messages(messages):
    for message in messages:
        # Hidden the keyboard with options of answers
        keyboard_hider = types.ReplyKeyboardRemove()
    # If the answer is right/wrong:
        if message.text == 'МАМИНА КУРТКА':
            bot.reply_to(message, 'Верно!', reply_markup=keyboard_hider)
        if message.text == 'СНЕГАМ СТАТЬ':
            bot.reply_to(message, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        if message.text == 'общество':
            klavirni(message)
        if message.text == 'кротокрыс':
            klavirni(message)


def klavirni(message):
    if message.text == 'общество':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text='посети)', url='http://beon.ru/')
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Приглашаю Посетить т.н. сайт beon", reply_markup=keyboard)
    if message.text == 'кротокрыс':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text='ВИиирАлл!!!',
                                                url='http://hdrezka.ag/animation/drama/11055-gurren-lagann.html')
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "катлету буш?", reply_markup=keyboard)


@bot.message_handler(commands=['test'])
def finds_file_ids(message):
    for file in os.listdir("music/"):
        if file.split('.')[-1] == 'ogg':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None)
            # send file_id:
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['game'])
def game(message):
    # Connection to DB
    db_worker = SQLighter(config.database_name)
    # GET random row from DB
    row = db_worker.select_single(random.randint(1, utilsss.get_rows_count()))
    # Creating the markup
    markup = utilsss.generate_markup(row[2], row[3])
    # Send audio file with options of answers
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Enable 'game' mode
    utilsss.set_user_game(message.chat.id, row[2])
    answer = utilsss.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Промазалы_))')
    #handle_messages(message)
    # Delete user from storage cus game is over
    utilsss.finish_user_game(message.chat.id)
    bot.send_message(message.chat.id, 'qq')
    # Disconnect from the DB
    db_worker.close()


@bot.message_handler(commands=['hi'])
def hi(message):
    bot.send_message(message.chat.id, 'hi buddy!')


@bot.message_handler(commands=['goose'])
def goose(message):
    file = random.randint(1, 21)
    photo = open('goose/' + str(file) + '.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    

@bot.message_handler(commands=['knb'])
def knb(message):
    file = random.randint(1,3)
    photo = open('knb/' + str(file) + '.png', 'rb')
    bot.send_photo(message.chat.id, photo)

    
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    matches = re.match(pattern, query.query)  # find some pattern in query
    if matches:
        try:
            s_b = random.randint(0, 100)
            r_sum = types.InlineQueryResultArticle(
                id='1', title='Покурить банок',
                description='Вероятность: {!s}'.format(s_b),
                input_message_content=types.InputTextMessageContent(
                    message_text="Вероятность покурить банок сегодня {!s}%".format(s_b))
                )

            b_c = random.randint(0, 100)
            r_sub = types.InlineQueryResultArticle(
                id='2', title='Вырубить дорогу',
                description='Вероятность: {!s}'.format(b_c),
                input_message_content=types.InputTextMessageContent(
                    message_text="Вероятность вырубить дорогу сегодня {!s}%".format(b_c))
                )

            d_b = random.randint(0, 100)
            r_div = types.InlineQueryResultArticle(
                id='3', title='Нахуярится водкой+пиво',
                description="Вероятность: {!s}".format(d_b),
                input_message_content=types.InputTextMessageContent(
                    message_text="Вероятность нахуярится водкой+пиво сегодня {!s}%".format(d_b))
                )

            u_s = random.randint(0, 5)
            r_mul = types.InlineQueryResultArticle(
                id='4', title='Юзануть солей',
                description='Вероятность: {!s}'.format(u_s),
                input_message_content=types.InputTextMessageContent(
                    message_text='Вероятность юзануть солей сегодня {!s}%'.format(u_s))
                )

            bot.answer_inline_query(query.id, [r_sum, r_sub, r_div, r_mul])

        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))


@bot.inline_handler(func=lambda query: len(query.query) is 0)
def empty_query(query):
    hint = 'Введите news и узнайте какие сегодня дела'
    try:
        r = types.InlineQueryResultArticle(
            id='1',
            title='Бот \"Дела"',
            description=hint,
            input_message_content=types.InputTextMessageContent(
                message_text='Нужно ввести news')
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)
        
        
if __name__ == '__main__':
    
    utilsss.count_rows()
    random.seed()
    bot.set_update_listener(handle_messages)
    bot.polling(none_stop=False, interval=0, timeout=20)
