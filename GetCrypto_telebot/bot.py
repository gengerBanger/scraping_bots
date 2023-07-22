from parser import *
from config import TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(token=TOKEN)

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_OneCoin = types.KeyboardButton(text='/OneCoin')
button_top15 = types.KeyboardButton(text='/top15')
button_top100 = types.KeyboardButton(text='/top100')
update = types.KeyboardButton(text='/update_the_data')
clear = types.KeyboardButton(text='/clear')
main_keyboard.add(button_OneCoin, button_top15, button_top100, update, clear)

buffer_of_messagesID = list()
def uptade_the_data(chat_id):
    load = bot.send_message(chat_id=chat_id, text='⌛Подождите, данные собираются⌛').id
    main_parser()
    bot.delete_message(chat_id, load)
    sendKeyboard(chat_id)
def sendKeyboard(id):
    buffer_of_messagesID.append(bot.send_message(chat_id=id, text='⌨Выбери функцию⌨', reply_markup=main_keyboard).id)

@bot.message_handler(commands=['clear'])
def clear_chat(message: types.Message):
    chat_id = message.chat.id
    buffer_of_messagesID.append(message.message_id)
    for message_id in buffer_of_messagesID:
        bot.delete_message(chat_id, message_id)
    buffer_of_messagesID.clear()
@bot.message_handler(commands=['start', 'help'])
def on_start(message: types.Message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    buffer_of_messagesID.append(message.id)
    inline_key = types.InlineKeyboardMarkup()
    ref_button = types.InlineKeyboardButton(text='Coin Market Cap', url=URL)
    inline_key.add(ref_button)
    buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text=f'Привет, {name}🖐\n\n Здесь ты можешь получить актуальную информацию'
                                           f' по курсу, изменениям и капитализации криптовалют🤑\n\n'
                                           f'🤖На данный момент мой функционал позволяет:\n\n'
                                           f'1️⃣ Вывести полную информацию о монете по ее названию\n\n'
                                           f'2️⃣ Показать топ 15 монет по положительным изменениям за час / день / месяц\n\n'
                                           f'3️⃣ Отправить csv файл с полной информацией о каждой монете, входящей в топ 100 по общей капитализации\n\n'
                                           f'Данные берутся с сайта\n 📊Coin Market Cap📊', reply_markup=inline_key).id)
    uptade_the_data(chat_id)
def get_OneCoinInf(message: types.Message):
    message_text = message.text
    buffer_of_messagesID.append(message.id)
    chat_id = message.chat.id
    for coin in coins:
        if coin == message_text:
            prise = coins[coin]['price']
            h1 = coins[coin]['changes per hour']
            h24 = coins[coin]['changes per day']
            week = coins[coin]['changes per week']
            capitalization = coins[coin]['market capitalization']
            answer = f'💰Cтоимость монеты💰 {coin} = {prise}\n\n' \
                     f'Изменение за час : {h1}\n\n' \
                     f'Изменение за день : {h24}\n\n' \
                     f'Изменение за неделю : {week}\n\n' \
                     f'💸Капитализация💸 : {capitalization}'
            buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text=answer).id)
            sendKeyboard(chat_id)
            break
    else:
        buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text='❗Монета не найдена❗').id)

@bot.message_handler(commands=['OneCoin'])
def one_coin_inf(message: types.Message):
    chat_id = message.chat.id
    buffer_of_messagesID.append(message.id)
    buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text='Введи название монеты ❗заглавными буквами❗').id)
    bot.register_next_step_handler(message, get_OneCoinInf)
def get_info_top15(parameter):
    hourDict = {}
    for coin in coins:
        hourDict[coin] = coins[coin][parameter][:len(coins[coin][parameter]) - 1]
        if hourDict[coin][0] == '+':
            hourDict[coin] = float(hourDict[coin][1:])
        else:
            hourDict[coin] = float(hourDict[coin])
    newhourDict = dict(sorted(hourDict.items(), key=lambda x: x[1], reverse=True))
    answer = ''
    count = 1
    for item in newhourDict:
        answer += f'{count}) {item} : {newhourDict[item]}\n\n'
        count += 1
        if count == 16:
            break
    return answer
def get_top15(message: types.Message):
    buffer_of_messagesID.append(message.id)
    chat_id = message.chat.id
    match message.text:
        case 'ЧАС':
            buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text=get_info_top15('changes per hour')).id)
        case 'ДЕНЬ':
            buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text=get_info_top15('changes per day')).id)
        case 'НЕДЕЛЯ':
            buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text=get_info_top15('changes per week')).id)
    sendKeyboard(chat_id)
@bot.message_handler(commands=['top15'])
def top15_inf(message: types.Message):
    chat_id = message.chat.id
    buffer_of_messagesID.append(message.id)
    buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text='Введи временной промежуток (ЧАС / ДЕНЬ / НЕДЕЛЯ)\n'
                                                                       '❗заглавными буквами❗').id)
    bot.register_next_step_handler(message, get_top15)

@bot.message_handler(commands=['top100'])
def top100_inf(message: types.Message):
    chat_id = message.chat.id
    buffer_of_messagesID.append(message.id)
    save_csv(storage, coins)
    file = open('result.csv', 'rb')
    buffer_of_messagesID.append(bot.send_document(chat_id=chat_id, document=file).id)
    file.close()

@bot.message_handler(commands=['update_the_data'])
def update(message: types.Message):
    chat_id = message.chat.id
    buffer_of_messagesID.append(message.id)
    uptade_the_data(chat_id)
    buffer_of_messagesID.append(bot.send_message(chat_id=chat_id, text='📋Данные обновлены📋').id)

if __name__ == '__main__':
    bot.infinity_polling()
