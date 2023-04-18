import telebot
from telebot import types

from api import Trans, Rate
from config import *

dct = {  # Главный словарь, по пунктам которого будет выполняться API запрос
    'from': '',
    'for': '',
    'count': '',
    'first_message_1': True,
    'first_message_2': True,
    'first_message_3': True
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """Функция, которая будет выполняться, при комманде start"""
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)  # Удаляем верхнее сообщение
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем сетку для главных кнопочек
    item1 = types.KeyboardButton(GIT_HUB_KEY)  # Создаем кнопочку
    item2 = types.KeyboardButton(TRANS_KEY)  # Создаем кнопочку
    item3 = types.KeyboardButton(RATE_KEY)  # Создаем кнопочку
    markup.add(item1)  # Добавляем кнопочку1 к сетке
    markup.add(item2, item3)  # Добавляем кнопочку2 и кнопочку3 к сетке
    bot.send_message(message.chat.id, START,
                     reply_markup=markup, parse_mode='HTML')  # Отправляем сообщение приветствие START


@bot.message_handler(content_types=['text'])
def trans(message):
    """Функция, которая будет выполняться, при ЛЮБОМ сообщении"""
    user_message = message.text  # Что отправил пользователь
    if user_message == GIT_HUB_KEY:
        dct['first_message_2'] = False
        dct['first_message_3'] = False
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if not dct['first_message_1']:
            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.message_id - 1)  # Удаляем верхнее сообщение
        text = GIT_HUB_KEY
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text='тык.',
                                           url=GIT_HUB_VALUE)  # При нажатии на кнопку будет открывать ссылка
        markup.add(item1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif user_message == TRANS_KEY:
        dct['first_message_1'] = False
        dct['first_message_3'] = False
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)  # Удаляем верхнее сообщение
        if not dct['first_message_2']:
            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.message_id - 1)  # Удаляем верхнее сообщение
        markup = types.InlineKeyboardMarkup()  # Создаем сетку для кнопочек под сообщением

        item1 = types.InlineKeyboardButton(text=RUB,
                                           callback_data='trans_from_rub')  # Создаем кнопочку
        item2 = types.InlineKeyboardButton(text=USD,
                                           callback_data='trans_from_usd')  # Создаем кнопочку
        item3 = types.InlineKeyboardButton(text=EUR,
                                           callback_data='trans_from_eur')  # Создаем кнопочку
        # callback_data принимаем название колбэк, и отправляет его, при нажатии на кнопку
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, FROM, reply_markup=markup, parse_mode='HTML')
    elif user_message == RATE_KEY:
        dct['first_message_1'] = False
        dct['first_message_2'] = False
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)  # Удаляем верхнее сообщение
        if not dct['first_message_3']:
            bot.delete_message(chat_id=message.chat.id,
                               message_id=message.message_id - 1)  # Удаляем верхнее сообщение

        rate = Rate()
        rate_usd, rate_eur = rate.get_rates()
        rate_today_message = RATE_TODAY.format(rate_usd=rate_usd, rate_eur=rate_eur)
        bot.send_message(message.chat.id, rate_today_message, parse_mode='HTML')
    else:
        user_message = message.text  # Что отправил пользователь
        if user_message.isdigit():  # Если сообщение число
            if dct.get('from', False) and dct.get('for', False):  # Если заполнен словарь
                if dct.get('count', False) == 'another':  # Если в словаре another
                    dct['count'] = user_message

                    output_result(message)  # Вызываем функцию подсчета результата
                else:
                    bot.send_message(message.chat.id, WRONG_COMMAND)
                    start(message)
            else:
                bot.send_message(message.chat.id, WRONG_COMMAND)
                start(message)
        else:
            bot.send_message(message.chat.id, WRONG_COMMAND)
            start(message)


@bot.callback_query_handler(func=lambda call: True)
def trans(call):
    """Функция, которая принимаем callback"""
    call_back = call.data  # Получить текст call_back
    if call_back in ['trans_from_rub', 'trans_from_usd', 'trans_from_eur']:
        item1, item2, item3 = None, None, None
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        if call_back == 'trans_from_rub':
            dct['from'] = 'rub'
            item1 = types.InlineKeyboardButton(text=USD, callback_data='trans_for_usd')
            item2 = types.InlineKeyboardButton(text=EUR, callback_data='trans_for_eur')
            item3 = types.InlineKeyboardButton(text=BACK, callback_data='trans_back')

        elif call_back == 'trans_from_usd':
            dct['from'] = 'usd'
            item1 = telebot.types.InlineKeyboardButton(text=RUB, callback_data='trans_for_rub')
            item2 = telebot.types.InlineKeyboardButton(text=EUR, callback_data='trans_for_eur')
            item3 = telebot.types.InlineKeyboardButton(text=BACK, callback_data='trans_back')

        elif call_back == 'trans_from_eur':
            dct['from'] = 'eur'
            item1 = telebot.types.InlineKeyboardButton(text=RUB, callback_data='trans_for_rub')
            item2 = telebot.types.InlineKeyboardButton(text=USD, callback_data='trans_for_usd')
            item3 = telebot.types.InlineKeyboardButton(text=BACK, callback_data='trans_back')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, FOR, reply_markup=markup)
    elif call_back in ['trans_for_rub', 'trans_for_usd', 'trans_for_eur']:
        markup = types.InlineKeyboardMarkup()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        item1 = telebot.types.InlineKeyboardButton(text=BACK, callback_data='trans_back_2')
        item2 = telebot.types.InlineKeyboardButton(text=ANOTHER_KEY,
                                                   callback_data='count_another')
        item3 = telebot.types.InlineKeyboardButton(text='5', callback_data='count_5')
        item4 = telebot.types.InlineKeyboardButton(text='10', callback_data='count_10')
        item5 = telebot.types.InlineKeyboardButton(text='50', callback_data='count_50')
        item6 = telebot.types.InlineKeyboardButton(text='100', callback_data='count_100')
        item7 = telebot.types.InlineKeyboardButton(text='1000', callback_data='count_1000')
        item8 = telebot.types.InlineKeyboardButton(text='5000', callback_data='count_5000')
        if call_back == 'trans_for_rub':  # Если кнопка Перевести в rub
            dct['for'] = 'rub'
        elif call_back == 'trans_for_usd':  # Если кнопка Перевести в uds
            dct['for'] = 'usd'
        elif call_back == 'trans_for_eur':  # Если кнопка Перевести в eur
            dct['for'] = 'eur'
        markup.add(item1, item2)
        markup.add(item3, item4, item5)
        markup.add(item6, item7, item8)
        bot.send_message(call.message.chat.id, 'Количество?', reply_markup=markup)

    elif call_back in ['count_5', 'count_10', 'count_50', 'count_100', 'count_1000', 'count_5000']:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call_back == 'count_5':
            dct['count'] = '5'
        elif call_back == 'count_10':
            dct['count'] = '10'
        elif call_back == 'count_50':
            dct['count'] = '50'
        elif call_back == 'count_100':
            dct['count'] = '100'
        elif call_back == 'count_1000':
            dct['count'] = '1000'
        elif call_back == 'count_5000':
            dct['count'] = '5000'

        output_result(call.message)

    elif call_back == 'count_another':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        dct['count'] = 'another'
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text=RESET_KEY, callback_data='trans_back')
        markup.add(item1)
        bot.send_message(call.message.chat.id, ANOTHER_VALUE, reply_markup=markup)

    elif call_back == 'trans_back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        text = FROM
        dct['from'] = ''
        dct['for'] = ''
        dct['count'] = ''
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text=RUB, callback_data='trans_from_rub')
        item2 = types.InlineKeyboardButton(text=USD, callback_data='trans_from_usd')
        item3 = types.InlineKeyboardButton(text=EUR, callback_data='trans_from_eur')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, text, reply_markup=markup)

    elif call_back == 'trans_back_2':
        valut_from = dct['from']
        dct['for'] = ''
        dct['count'] = ''
        item1, item2, item3 = None, None, None
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup()

        if valut_from == 'rub':
            item1 = types.InlineKeyboardButton(text=USD, callback_data='trans_for_usd')
            item2 = types.InlineKeyboardButton(text=EUR, callback_data='trans_for_eur')
            item3 = types.InlineKeyboardButton(text=BACK, callback_data='trans_back')

        elif valut_from == 'usd':
            item1 = telebot.types.InlineKeyboardButton(text=RUB, callback_data='trans_for_rub')
            item2 = telebot.types.InlineKeyboardButton(text=EUR, callback_data='trans_for_eur')
            item3 = telebot.types.InlineKeyboardButton(text=BACK, callback_data='trans_back')

        elif valut_from == 'eur':
            item1 = telebot.types.InlineKeyboardButton(text=RUB, callback_data='trans_for_rub')
            item2 = telebot.types.InlineKeyboardButton(text=USD, callback_data='trans_for_usd')
            item3 = telebot.types.InlineKeyboardButton(text=BACK, callback_data='trans_back')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(call.message.chat.id, FOR, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, WRONG_COMMAND)
        start(call.message)

def output_result(message):
    dct['first_message_1'] = True
    dct['first_message_2'] = True
    dct['first_message_3'] = True

    """Функция подсчета и вывода результата"""
    from_ = dct['from'].upper()
    to_ = dct['for'].upper()
    amount_ = dct['count'].upper()

    res = Trans(from_=from_, to_=to_,
                    amount_=amount_)  # Вызывается класс GetResult, который принимает 3 параметра
    result_ = res.get_result()  # Вызывает метод, который высчитывает результат

    result_message = RESULT.format(amount_=amount_, from_=from_, to_=to_, result_=result_)

    bot.send_message(message.chat.id, result_message, parse_mode='HTML')


if __name__ == '__main__':
    print(START_MESSAGE)
    bot.polling(none_stop=True)  # Работа бота
