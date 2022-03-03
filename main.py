import random
import re

import telebot.types

from config import *
from flask import Flask
from keyboardlist import *
from FilmList import *
import time
from thumb_url import *
from img_funcs import *
import os

bot = telebot.TeleBot(TOKEN)  # Мой токен

app = Flask(__name__)
conf_db = config_for_db


@bot.message_handler(commands=['start'])
def start_message(message):
    cid = message.chat.id
    with open('id_list.txt', 'r') as file:
        id_list = file.read().split('\n')
    with open('tmp_id_list.txt', 'r') as file:
        tmp_id_list = file.read().split('\n')

    if str(cid) not in id_list:
        with open('id_list.txt', 'a') as file:
            file.write(str(cid) + '\n')
        if str(cid) not in tmp_id_list:
            with open('tmp_id_list.txt', 'a') as file:
                file.write(str(cid) + '\n')

    if cid == my_id:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Предложка', callback_data='markup1'))
        markup.add(telebot.types.InlineKeyboardButton(text='Новые пользователи', callback_data='markup2'))
        markup.add(telebot.types.InlineKeyboardButton(text='Пользователей всего', callback_data='markup3'))
        markup.add(telebot.types.InlineKeyboardButton(text='Отпрвить сообщение всем', callback_data='markup4'))
        bot.send_message(message.chat.id, 'Здарова!', reply_markup=markup)
    bot.send_message(message.chat.id,
                     'Привет, если нужен годный фильм, то ты по адресу. Коллекция фильмов пока еще небольшая, '
                     'но я над ней работаю. Ты можешь помочь: небольшое описание к любимому фильму или реквест на '
                     'фильм, который ты считаешь крутым можешь смело добавлять! @rovo0',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'в начало':
        bot.send_message(message.chat.id, 'Меню', reply_markup=keyboard1)

    if message.text.lower() == 'подобрать':
        # Подобрать фильм
        bot.send_message(message.chat.id, '*', reply_markup=keyboard2)

    if message.text.lower() == 'cлучайный':
        # Случайный фильм
        random_film = film_list(conf_db)[random.randint(0, len(film_list(conf_db)) - 1)]
        path = open('photo/{}.JPEG'.format(random_film[0]), 'rb')
        text_message = '\n'.join(random_film)
        bot.send_photo(message.chat.id, path)
        bot.send_message(message.chat.id, text_message, reply_markup=keyboard3)

    if message.text.lower() == 'ещё':
        # Еще
        random_film = film_list(conf_db)[random.randint(0, len(film_list(conf_db)) - 1)]
        path = open('photo/{}.JPEG'.format(random_film[0]), 'rb')
        text_message = '\n'.join(random_film)
        bot.send_photo(message.chat.id, path)
        bot.send_message(message.chat.id, text_message, reply_markup=keyboard3)

    if message.text.lower() == 'назад':
        # 'Назад'
        bot.send_message(message.chat.id, 'назад', reply_markup=keyboard2)

    if message.text.lower() == 'по году':
        # Выборка по году
        markup = telebot.types.InlineKeyboardMarkup()
        for film in sorted([_ for _ in set(film_list_key(conf_db, 'year'))]):
            markup.add(telebot.types.InlineKeyboardButton(text=film[0], callback_data=film[0]))
        bot.send_message(message.chat.id, text="Выберите год", reply_markup=markup)

    if message.text.lower() == 'по режиссеру':
        # Выборка режиссеров
        markup = telebot.types.InlineKeyboardMarkup()
        for director in sorted([_ for _ in set(film_list_key(conf_db, 'director'))]):
            markup.add(telebot.types.InlineKeyboardButton(text=director[0], callback_data=director[0]))
        bot.send_message(message.chat.id, text="Выберите фильм, чтобы прочитать описание", reply_markup=markup)

    if message.text.title() in [_[0] for _ in film_list_key(conf_db, 'director')]:  # Подбор фильмов режиссера
        markup = telebot.types.InlineKeyboardMarkup()
        for film in film_list(conf_db):
            if message.text.title() == film[1]:
                markup.add(telebot.types.InlineKeyboardButton(text=film[0], callback_data=film[0]))
        bot.send_message(message.chat.id, 'Введите название фильма, чтобы прочитать описание',
                         reply_markup=keyboard4)

    if message.text.lower() == 'по жанру':
        # Список жанров
        bot.send_message(message.chat.id, 'Выберите жанр', reply_markup=keyboard5)

    if message.text.title() in [_[0] for _ in film_list_key(conf_db, 'genre')]:
        # Выборка по жанру
        markup = telebot.types.InlineKeyboardMarkup()
        for film in film_list(conf_db):
            if message.text.title() == film[4]:
                markup.add(telebot.types.InlineKeyboardButton(text=film[0], callback_data=film[0]))
        bot.send_message(message.chat.id, 'Выберите название фильма, чтобы прочитать описание',
                         reply_markup=markup)

    if message.text in [_[0] for _ in film_list_key(conf_db, 'name')]:
        for film in film_list(conf_db):
            text_message = '\n'.join(film)
            path = open('photo/{}.JPEG'.format(film[0]), 'rb')
            if message.text == film[0]:
                bot.send_photo(message.chat.id, path)
                bot.send_message(message.chat.id, text=text_message, reply_markup=keyboard4)

    if message.text.lower() == 'добавить':
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        """Просто отправляй сообщения по следующим пунктам: 
                                                                            Название фильма"""),
                                       callback=film_add_director)

    if message.text.lower() == 'годится!':
        with open('temp/{}.txt'.format(message.from_user.username), 'r') as file:
            text = file.read().split('\n')
        bot.send_message('447458089', '\n'.join(text))
        bot.send_photo('447458089', text[-1])
        bot.send_message(message.chat.id, 'Спасибо', reply_markup=keyboard4)

    if message.text.lower() == 'пробовать другое':
        with open('temp/{}.txt'.format(message.from_user.username), 'r') as file:
            content = file.read().split()[0]
        with open('temp/{}.txt'.format(message.from_user.username), 'a') as file:
            file.write('\n' + image_url(content + ' фильм')[1])
        bot.send_photo(message.chat.id, image_url(content + ' фильм')[1])
        bot.send_message(message.chat.id, 'Подходит? Если нет я подберу после сам.', reply_markup=keyboard7)

    if message.text.lower() == 'ссылка на фото':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Отправь мне ссылку'),
                                       callback=add_photo_url)


def add_photo_url(message):
    with open('temp/{}.txt'.format(message.from_user.username), 'a') as file:
        file.write('\n'+message.text)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.send_message(message.chat.id, 'Спасибо!', reply_markup=keyboard4)


def film_add_director(message):
    with open('temp/{}.txt'.format(message.from_user.username), 'w') as file:
        file.write(message.text.capitalize() + '\n')
    if message.text.title() in [film[0] for film in film_list_key(conf_db, 'name')]:
        bot.send_message(message.chat.id, 'Такой фильм уже есть', reply_markup=keyboard1)
        bot.clear_step_handler_by_chat_id(message.chat.id)
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Имя режиссера'), callback=film_add_year)


def film_add_year(message):
    with open('temp/{}.txt'.format(message.from_user.username), 'a') as file:
        file.write(message.text.title() + '\n')
    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Год'), callback=film_add_description)


def film_add_description(message):
    with open('temp/{}.txt'.format(message.from_user.username), 'a') as file:
        file.write(message.text.title() + '\n')
    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Описание'), callback=film_add_genre)


def film_add_genre(message):
    with open('temp/{}.txt'.format(message.from_user.username), 'a') as file:
        file.write(message.text + '\n')
    bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                    'Жанр:\nДрама\nКомедия\nУжасы\nТриллер\nВестерн\nБоевик\nФантистика'
                                                    ), callback=film_add_photo)


def film_add_photo(message):
    with open('temp/{}.txt'.format(str(message.from_user.username)), 'a') as file:
        file.write(message.text + '\n')
    with open('temp/{}.txt'.format(str(message.from_user.username)), 'r') as file:
        content = file.read().split('\n')[0]
    with open('temp/{}.txt'.format(str(message.from_user.username)), 'a') as file:
        file.write(image_url(content + ' фильм')[0])
    bot.send_photo(message.chat.id, image_url(content + ' фильм')[0])
    bot.send_message(message.chat.id, 'Подходит?', reply_markup=keyboard7)
    bot.clear_step_handler_by_chat_id(message.chat.id)


def send_message_to_all(message):
    with open('id_list.txt', 'r') as file:
        id_list = file.read().split()
    for _id in id_list:
        bot.send_message(_id, message.text)
        time.sleep(.25)
    bot.clear_step_handler_by_chat_id(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)  # Инлайн кнопки
def query_handler(call):
    if call.data in [_[0] for _ in film_list_key(conf_db, 'year')]:
        markup = telebot.types.InlineKeyboardMarkup()
        for film in film_list(conf_db):
            if call.data == film[2]:
                markup.add(
                    telebot.types.InlineKeyboardButton(film[0], callback_data=film[0]))
        bot.send_message(call.message.chat.id, 'Выберите фильм', reply_markup=markup)

    if call.data in [_[0] for _ in film_list(conf_db)]:  # Вывод фильма по call.data
        for film in film_list(conf_db):
            if call.data == film[0]:
                path = open('photo/{}.JPEG'.format(film[0]), 'rb')
                bot.send_photo(call.message.chat.id, path)
                bot.send_message(call.message.chat.id,
                                 '\n'.join([_ for _ in film]),
                                 reply_markup=keyboard4)

    if call.data in [_[0] for _ in film_list_key(conf_db, 'director')]:  # Инлайн кнопки 'По-режиссеру'
        markup = telebot.types.InlineKeyboardMarkup()
        for film in film_list(conf_db):
            if call.data == film[1]:
                markup.add(
                    telebot.types.InlineKeyboardButton(film[0], callback_data=film[0]))
        bot.send_message(call.message.chat.id, 'Выберите фильм', reply_markup=markup)

    if call.data == 'markup1':
        markup = telebot.types.InlineKeyboardMarkup()
        path = 'temp/'
        for filename in os.listdir(path):
            markup.add(telebot.types.InlineKeyboardButton(filename, callback_data=filename))
        bot.send_message(call.message.chat.id, 'список предложки', reply_markup=markup)

    if call.data in [filename for filename in os.listdir('temp/')]:
        file = open('temp/{}'.format(call.data), 'r')
        content = [name for name in file.read().split('\n')]
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('да', callback_data='PUSH CONTENT' + call.data))
        markup.add(telebot.types.InlineKeyboardButton('нет', callback_data='DELETE CONTENT' + call.data))
        try:
            bot.send_photo(call.message.chat.id, content[-1])

        except Exception as e:
            bot.send_message(call.message.chat.id, 'Нет url фото в файле')
            time.sleep(5)
        bot.send_message(call.message.chat.id, '\n'.join(content[-2::-1]), reply_markup=markup)

    if 'PUSH CONTENT' in call.data:
        with open('temp/' + call.data.split('PUSH CONTENT')[1], 'r') as file_:
            content = file_.read().split('\n')
        img_download(content[-1], content[0])
        push_content(conf_db, content)
        push_thumb(content[0])
        os.remove('temp/' + call.data.split('PUSH CONTENT')[1])
        os.remove('photo/' + content[0] + '_thumb.JPEG')
        bot.send_message(call.message.chat.id, 'готово')

    if 'DELETE CONTENT' in call.data:
        os.remove('temp/' + call.data.split('DELETE CONTENT')[1])
        bot.send_message(call.message.chat.id, 'удалено')

    if call.data == 'markup2':
        with open('tmp_id_list.txt', 'r') as file:
            count = len(file.read().split())
        with open('tmp_id_list.txt', 'w') as file:
            file.write('')
        bot.send_message(call.message.chat.id, str(count - 1))

    if call.data == 'markup3':
        with open('id_list.txt', 'r') as file:
            number = file.read().split()
        bot.send_message(call.message.chat.id, str(len(number) - 1))

    if call.data == 'markup4':
        bot.register_next_step_handler(bot.send_message(call.message.chat.id, 'Пиши'), callback=send_message_to_all)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    string_pattern = re.compile(r'.')
    matches = re.match(string_pattern, query.query)
    messages = []
    counter = 0
    if matches:
        for name in film_list_key(conf_db, 'name'):
            if re.match(query.query.lower(), name[0].lower()):
                messages.append(telebot.types.InlineQueryResultArticle(
                    id=str(counter),
                    title=name[0],
                    description=str(len(messages) + 1),
                    input_message_content=telebot.types.InputTextMessageContent(
                        message_text=name[0]
                    ),
                    thumb_url=get_thumb_url(name[0]), thumb_width=48, thumb_height=48,
                ))
            counter += 1
        bot.answer_inline_query(query.id, results=messages)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)
