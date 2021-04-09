import json

import gspread
import requests
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types

bot = telebot.TeleBot("1755010290:AAEzTJ7k5gQJCIQiDEjVIiEkEsm9YPpthpE")


def active_app(app_number):
    text_app = ''
    for el in app_number:
        text_app += info(el) + "\n"
    return text_app


def info_app(app, index, j):
    arr = []
    for el in app:
        app_status.append(el.get('Статус'))
        app_store.append(el.get('Площадка'))
        if app_status[len(app_status) - 1] == status[index] and app_store[len(app_store) - 1] == store[j]:
            arr.append(el.get('ID'))
        else:
            continue
    return arr


def info(index):
    info_application = ''
    row = sheet.row_values(index + 1)
    if not row[4]:
        info_application += '\nНомер приложения - ' + row[0] + '\nНазвание - ' + row[5] + '\nСтрана ' + row[2] \
                            + '\nПлощадка ' + row[3] + '\nТип приложения ' + row[
                                12] + '\nСсылка на приложение - ' + 'Ссылка отсутствует'
    else:
        info_application += '\nНомер приложения - ' + row[0] + '\nНазвание - ' + row[5] + '\nСтрана ' + row[2] \
                            + '\nПлощадка ' + row[3] + '\nТип приложения ' + row[
                                12] + '\nСсылка на приложение - ' + row[4]
    return info_application


def response_of(message, url):
    response = requests.get(url)
    if not response.text:
        offer_url = 'оффер пустой   ' + url
        bot.send_message(message.chat.id, offer_url)

    elif response.status_code == 200:
        offer_url = 'Все хорошо  ' + url
        bot.send_message(message.chat.id, offer_url)

    else:
        offer_url = "какие-то проблемы" + url + "код ошибки" + response.status_code
        bot.send_message(message.chat.id, offer_url)


def response_screen(message, url):
    req = requests.get(url)
    if req.status_code == 200:
        string = '' + url + '\n'
        bot.send_message(message.chat.id, string)

    else:
        error(message, req)


def create_markup(markups):
    markup = types.ReplyKeyboardMarkup(True)
    for x in markups:
        markup.add(*x)
    return markup


def active_app(app_number):
    text_app = ''
    for el in app_number:
        text_app += info(el) + "\n"
    return text_app


def build_text(index, j, app_number):
    text = text_template[index] + " " + store[j] + active_app(app_number)
    return text


def check_app_offer(message):
    markup = create_markup([[' Назад ']])
    msg = bot.send_message(message.chat.id, 'Введите номер приложения, которое вы хотите проверить',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, get_text_messages)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    msg = bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(msg, send_welcome)


def send_welcome(message):
    if message.text == '1234567':
        markup = create_markup(
            [["Посмотреть список всех активных приложений", "Список приложений в анализе крашей"],
             ['Список неопубликованных приложений', "Список приложений в разработке"],
             ["Список приложений заготовок", "Проверить офферы у приложения"],
             ['Узнать все об одном приложении']])
        msg = bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
        bot.register_next_step_handler(msg, get_choose_act)
    else:
        msg = bot.send_message(message.chat.id, "НУ ПАРОЛЬ ВЫ НЕ УГАДАЛИ")
        bot.register_next_step_handler(msg, start)


def back_button(message):
    markup = create_markup(
        [["Посмотреть список всех активных приложений", "Список приложений в анализе крашей"],
         ['Список неопубликованных приложений', "Список приложений в разработке"],
         ["Список приложений заготовок", "Проверить офферы у приложения"],
         ['Узнать все об одном приложении']])
    msg = bot.send_message(message.chat.id, 'Выберите действие ', reply_markup=markup)
    bot.register_next_step_handler(msg, get_choose_act)


def choose_method(message):
    markup = create_markup([["Назад"]])
    msg = bot.send_message(message.chat.id, 'Введите номер приложения', reply_markup=markup)
    if message.text == "Проверить с выводом офферов":
        bot.register_next_step_handler(msg, get_text_messages)
    else:
        bot.register_next_step_handler(msg, get_offers)


def get_choose_act(message):
    text = ''
    markup = create_markup([["Назад"]])
    size = len(text)
    if message.text == "Посмотреть список всех активных приложений":
        for i in range(4):
            if not not app[i]:
                text += build_text(0, i, app[i])
                if len(text) < 4096:
                    size = len(text)
        if len(text) > size:
            for x in range(0, len(text), size):
                msg = bot.send_message(message.chat.id, text[x:x + size], reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, back_button)
        print(size)
    elif message.text == "Список приложений в анализе крашей":
        for i in range(5, 10):
            if not not app[i]:
                text = build_text(1, i - 5, app[i])
                if len(text) < 4096:
                    size = len(text)
            if len(text) > size:
                for x in range(0, len(text), size):
                    msg = bot.send_message(message.chat.id, text[x:x + size], reply_markup=markup)
            else:
                msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, back_button)
    elif message.text == "Список приложений заготовок":
        for i in range(10, 15):
            if not not app[i]:
                text += build_text(2, i - 10, app[i])
                if len(text) < 4096:
                    size = len(text)
        if len(text) > size:
            for x in range(0, len(text), size):
                msg = bot.send_message(message.chat.id, text[x:x + size], reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, back_button)
    elif message.text == 'Список неопубликованных приложений':
        for i in range(15, 20):
            if not not app[i]:
                text += build_text(3, i - 15, app[i])
                if len(text) < 4096:
                    size = len(text)
        if len(text) > size:
            for x in range(0, len(text), size):
                msg = bot.send_message(message.chat.id, text[x:x + size], reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, back_button)
    elif message.text == "Список приложений в разработке":
        for i in range(20, 25):
            if not not app[i]:
                text += build_text(4, i - 20, app[i])
                if len(text) < 4096:
                    size = len(text)
        if len(text) > size:
            for x in range(0, len(text), size):
                msg = bot.send_message(message.chat.id, text[x:x + size], reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, back_button)
    elif message.text == "Проверить офферы у приложения":
        markup = create_markup([['Проверить с выводом офферов'],
                                ['Проверить без вывода']])
        msg = bot.send_message(message.chat.id, 'Выберете способ проверки приложения', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_method)
    elif message.text == "Узнать все об одном приложении":
        markup = create_markup([["Назад"]])
        msg = bot.send_message(message.chat.id, 'Введите номер приложения', reply_markup=markup)
        bot.register_next_step_handler(msg, info_one_app)


def all_info(index):
    info_application = ''
    row = sheet.row_values(index + 1)
    if not row[4]:
        info_application += '\nНомер приложения - ' + row[0] + '\nНазвание - ' + row[5] + '\nСтрана' + row[2] \
                            + '\n Площадка ' + row[3] + '\nТип приложения ' + row[
                                12] + '\nОбфускация ' + row[10] + '\nДизайн ' + row[7] + '\nИконка ' + row[
                                11] + '\nМетрика ' + row[6] + '\nСсылка на приложение - ' + 'Ссылка отсутствует'
    else:
        info_application += '\nНомер приложения - ' + row[0] + '\nНазвание - ' + row[5] + '\nСтрана' + row[2] \
                            + '\nПлощадка ' + row[3] + '\nТип приложения ' + row[
                                12] + '\nОбфускация ' + row[10] + '\nДизайн ' + row[7] + '\nИконка ' + row[
                                11] + '\nМетрика ' + row[6] + '\nСсылка на приложение - ' + row[4]
    return info_application


def info_one_app(message):
    text = all_info(int(message.text))
    bot.send_message(message.chat.id, text)
    get_offers(message)


def get_offers(message):
    text = ''
    name = ''
    count = 0
    size = len(text)
    app_offer = []
    for el in data:
        app_offer.append(el.get('ID'))
        if app_offer[len(app_offer) - 1] == int(message.text):
            url = el.get('Ссылка на бек')
    response = requests.get(url)
    if response.status_code == 200:
        bot.send_message(message.chat.id, 'Сейчас все проверю')
        todos = json.loads(response.text)
        if todos.get('loans'):
            for item in todos.get("loans"):
                count += 1
                name += item.get('name') + ' - ' + item.get('order') + '\n'
            text += 'Займов - ' + str(count) + '\n' + name
            if len(text) < 4096:
                size = len(text)
            count = 0
            name = ''
        if todos.get('credits'):
            for item in todos.get("credits"):
                count += 1
                name += item.get('name') + ' - ' + item.get('order') + '\n'
            text += '\nКредитов - ' + str(count) + '\n' + name
            if len(text) < 4096:
                size = len(text)
            count = 0
            name = ''
        if todos.get('cards'):
            for index in todos.get('cards'):
                if index.get('cards_credit'):
                    for item in index.get("cards_credit"):
                        count += 1
                        name += item.get('name') + ' - ' + item.get('order') + '\n'
                    text += '\nКредитных карт - ' + str(count) + '\n' + name
                    if len(text) < 4096:
                        size = len(text)
                count = 0
                name = ''
                if index.get('cards_debit'):
                    for item in index.get("cards_debit"):
                        count += 1
                        name += item.get('name') + ' - ' + item.get('order') + '\n'
                    text += '\nДебитовых карт - ' + str(count) + '\n' + name
                    if len(text) < 4096:
                        size = len(text)
                count = 0
                name = ''
                if index.get('cards_installment'):
                    for item in index.get("cards_installment"):
                        count += 1
                        name += item.get('name') + ' - ' + item.get('order') + '\n'
                    text += '\nКарт рассрочек - ' + str(count) + '\n' + name
                    if len(text) < 4096:
                        size = len(text)
                count = 0
                name = ''
    else:
        error(message, response)
    if len(text) > size:
        for x in range(0, len(text), int(size)):
            bot.send_message(message.chat.id, text[x:x + int(size)])
    else:
        bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, back_button)


def error(message, response):
    bot.send_message(message.chat.id, 'Что-то ссылкой не так, вот статус код ', response.status_code)


def get_text_messages(message):
    app_offer = []
    for el in data:
        app_offer.append(el.get('ID'))
        if app_offer[len(app_offer) - 1] == int(message.text):
            url = el.get('Ссылка на бек')
    response = requests.get(url)
    if response.status_code == 200:
        bot.send_message(message.chat.id, 'Сейчас все проверю')
        todos = json.loads(response.text)
        if todos.get('loans'):
            for index in todos.get('loans'):
                response_of(message, index.get("order"))
                response_screen(message, index.get("screen"))
        if todos.get('credits'):
            for index in todos.get('credits'):
                response_of(message, index.get("order"))
                response_screen(message, index.get("screen"))
        if todos.get('cards'):
            for index in todos.get('cards'):
                if index.get('cards_credit'):
                    for j in index.get('cards_credit'):
                        response_of(message, j.get("order"))
                        response_screen(message, j.get("screen"))
                if index.get('cards_debit'):
                    for j in index.get('cards_debit'):
                        response_of(message, j.get("order"))
                        response_screen(message, j.get("screen"))
                if index.get('cards_installment'):
                    for j in index.get('cards_installment'):
                        response_of(message, j.get("order"))
                        response_screen(message, j.get("screen"))

    else:
        error(message, response)
    bot.register_next_step_handler(message, back_button)


scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file',
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open('CheckApp').sheet1

data = sheet.get_all_records()

data = sheet.get_all_records()

status = ['Живет', 'Анализ Крашей', 'Заготовка', 'Unpublish', 'Кодится']
store = ['GP', 'Samsung', 'Huawei', 'Xiaomi', 'iOS']

text_template = ["\n Живые приложения", "\n В анализе крашей", "\n Приложении заготовки",
                 "\n Не опубликованные приложения", "\n В разработке"]

app_status = []
app_store = []
app_number_live_gp = info_app(data, 0, 0)
app_number_live_smg = info_app(data, 0, 1)
app_number_live_hw = info_app(data, 0, 2)
app_number_live_ios = info_app(data, 0, 3)
app_number_live_mi = info_app(data, 0, 4)
app_number_test_gp = info_app(data, 1, 0)
app_number_test_smg = info_app(data, 1, 1)
app_number_test_hw = info_app(data, 1, 2)
app_number_test_ios = info_app(data, 1, 3)
app_number_test_mi = info_app(data, 1, 4)
app_number_new_gp = info_app(data, 2, 0)
app_number_new_smg = info_app(data, 2, 1)
app_number_new_hw = info_app(data, 2, 2)
app_number_new_ios = info_app(data, 2, 3)
app_number_new_mi = info_app(data, 2, 4)
app_number_unp_gp = info_app(data, 3, 0)
app_number_unp_smg = info_app(data, 3, 1)
app_number_unp_hw = info_app(data, 3, 2)
app_number_unp_ios = info_app(data, 3, 3)
app_number_unp_mi = info_app(data, 3, 4)
app_number_cod_gp = info_app(data, 4, 0)
app_number_cod_smg = info_app(data, 4, 1)
app_number_cod_hw = info_app(data, 4, 2)
app_number_cod_ios = info_app(data, 4, 3)
app_number_cod_mi = info_app(data, 4, 4)

app = [app_number_live_gp, app_number_live_smg, app_number_live_hw, app_number_live_ios, app_number_live_mi,
       app_number_test_gp, app_number_test_smg, app_number_test_hw, app_number_test_ios, app_number_test_mi,
       app_number_new_gp, app_number_new_smg, app_number_new_hw, app_number_new_ios, app_number_new_mi,
       app_number_unp_gp, app_number_unp_smg, app_number_unp_hw, app_number_unp_ios, app_number_unp_mi,
       app_number_cod_gp, app_number_cod_smg, app_number_cod_hw, app_number_cod_ios, app_number_cod_mi]

bot.polling(none_stop=True)
