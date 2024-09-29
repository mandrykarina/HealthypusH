# -*- coding: cp1251 -*-
# Импортируем необходимые классы.
import telebot
import sqlite3

HealthyPushbot = telebot.TeleBot('7521200493:AAGn6VBrEfsRGZSS79GmXt0S2RN-d4q95rI')

from telebot import types

#sqlite3
connection = sqlite3.connect("База_Данных.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS info')
cursor.execute('CREATE TABLE info(id INTEGER,age INTEGER,height INTEGER,weight INTEGER,gender INTEGER,lifestyle TEXT NOT NULL)')

@HealthyPushbot.message_handler(commands=['start'])
def startBot(message):
    id_ = message.from_user.id
    cursor.execute("DELETE FROM info WHERE id = ?", (id_,))
    message_out = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nЯ бот здорового питания HealthyPush. Готов начать путешествие в мир ЗОЖ?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text = 'Да', callback_data='Start_mess_yes'))
    cursor.execute("INSERT INTO info VALUES (?,-1,-1,-1,-1,?)",(message.from_user.id,"0"))
    connection.commit()
    HealthyPushbot.send_message(message.chat.id, message_out, parse_mode='html', reply_markup=markup)

@HealthyPushbot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "Start_mess_yes":
        message_out = "Отлично! Но я смогу тебе помочь, только если буду знать о тебе кое-что.\nДля начала, сколько тебе целых лет?"
        HealthyPushbot.send_message(function_call.message.chat.id, message_out)
        HealthyPushbot.answer_callback_query(function_call.id)
@HealthyPushbot.message_handler(content_types=['text'])
def answer_message(message):
    id_ = message.from_user.id
    age = int(cursor.execute("SELECT age FROM info WHERE id = ?", (id_,)).fetchone()[0])
    height = int(cursor.execute("SELECT height FROM info WHERE id = ?", (id_,)).fetchone()[0])
    weight = int(cursor.execute("SELECT weight FROM info WHERE id = ?", (id_,)).fetchone()[0])
    gender = int(cursor.execute("SELECT gender FROM info WHERE id = ?", (id_,)).fetchone()[0])
    lifestyle = cursor.execute("SELECT lifestyle FROM info WHERE id = ?", (id_,)).fetchone()[0]
    if age == -1:
        cursor.execute("UPDATE info SET age = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "Хорошо. Теперь мне нужно узнать твой рост."
    elif height == -1:
        cursor.execute("UPDATE info SET height = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "Отлично. Еще 4 вопроса. Теперь мне нужно узнать твой вес. Не беспокойся, это все останется между нами)"
    elif weight == -1:
        cursor.execute("UPDATE info SET weight = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "Записал. Теперь мне нужно узнать твой пол."
    elif gender == -1:
        if ('м' in message.text) or ('М' in message.text):
            cursor.execute("UPDATE info SET gender = ? WHERE id = ?", (0,id_,))
        else:
            cursor.execute("UPDATE info SET gender = ? WHERE id = ?", (1,id_,))
        connection.commit()
        message_out = "И последний вопрос. Какой у тебя образ жизни?"
    elif lifestyle == '0':
        cursor.execute("UPDATE info SET lifestyle = ? WHERE id = ?", (message.text,id_,))
        connection.commit()
        str_ = cursor.execute("SELECT age,height,weight,gender,lifestyle FROM info WHERE id = ?", (id_,)).fetchall()
        message_out = "Ура. Теперь мне известно все, что было необходимо.\nЧерех некоторое время у меня появится функционал и я тебе подскажу, как правильно питаться.\nПока!\n Записанные мною данные по твоему id:" + str(str_)
    HealthyPushbot.send_message(message.chat.id, message_out, parse_mode='html')

HealthyPushbot.infinity_polling()
