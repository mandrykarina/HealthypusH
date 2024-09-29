# -*- coding: cp1251 -*-
# ����������� ����������� ������.
import telebot
import sqlite3

HealthyPushbot = telebot.TeleBot('7521200493:AAGn6VBrEfsRGZSS79GmXt0S2RN-d4q95rI')

from telebot import types

#sqlite3
connection = sqlite3.connect("����_������.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS info')
cursor.execute('CREATE TABLE info(id INTEGER,age INTEGER,height INTEGER,weight INTEGER,gender INTEGER,lifestyle TEXT NOT NULL)')

@HealthyPushbot.message_handler(commands=['start'])
def startBot(message):
    message_out = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, ������!\n� ��� ��������� ������� HealthyPush. ����� ������ ����������� � ��� ���?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text = '��', callback_data='Start_mess_yes'))
    cursor.execute("INSERT INTO info VALUES (?,-1,-1,-1,-1,?)",(message.from_user.id,"0"))
    connection.commit()
    HealthyPushbot.send_message(message.chat.id, message_out, parse_mode='html', reply_markup=markup)

@HealthyPushbot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "Start_mess_yes":
        message_out = "�������! �� � ����� ���� ������, ������ ���� ���� ����� � ���� ���-���.\n ��� ������, ������� ���� ����� ���?"
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
        message_out = "������. ������ ��� ����� ������ ���� ����."
    elif height == -1:
        cursor.execute("UPDATE info SET height = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "�������. ��� 4 �������. ������ ��� ����� ������ ���� ���. �� ����������, ��� ��� ��������� ����� ����)"
    elif weight == -1:
        cursor.execute("UPDATE info SET weight = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "�������. ������ ��� ����� ������ ���� ���."
    elif gender == -1:
        cursor.execute("UPDATE info SET gender = ? WHERE id = ?", (int(message.text),id_,))
        connection.commit()
        message_out = "� ��������� ������. ����� � ���� ����� �����?"
    elif lifestyle == '0':
        cursor.execute("UPDATE info SET gender = ? WHERE id = ?", (message.text,id_,))
        connection.commit()
        str_ = cursor.execute("SELECT age,height,weight,gender,lifestyle FROM info WHERE id = ?", (id_,)).fetchall()
        message_out = "���. ������ ��� �������� ���, ��� ���� ����������.\n����� ��������� ����� � ���� �������� ���������� � � ���� ��������, ��� ��������� ��������.\n����!\n ���������� ���� ������ �� ������ id:" + str(str_)
    HealthyPushbot.send_message(message.chat.id, message_out, parse_mode='html')

HealthyPushbot.infinity_polling()