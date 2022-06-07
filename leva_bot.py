import telebot
import sqlite3
import requests

from dotenv import load_dotenv
import os

from send_db import send_to_db

from config import(
    start_text, create_card, create_questions,
    open_ooo, see_ofert, sample_power_of_attorney,
    open_card_text, create_request, main_page,
    request_text, question_text, sample_text, open_ooo_text,
    create_ooo_request, ooo_text, ok_load,
    ok_load_text, how_create_card, how_create_card_text,
    bank_open_bill_text, bank_open_bill, debet_bill_text,
    debet_bill, warranty, warranty_text, currency_bill_text,
    currency_bill, ofert_text, ofert, pay_button, ask_question,
    ask_question_text, wath_easy_vise, phone_number, address,
    send_data, load_adress, tarif, tarif_button, load_email
)

from keyBoards import (
    start_keyboard, CreateCardRequestKeyboard,
    RequestLoadKeyboard, QuestionKeyboard,
    SampeKeyboard, OooKeyboard, MainPageKeyBoard,
    HowCreateCardKeyboard, loadAddressKeyboard,
    loadPhoneKeyboard, loadEmailKeyboard

)

# from send_gmail import send_message_to_user_gmail

from payment_ym import pay, prepayment


db = sqlite3.connect("botUsers.db", check_same_thread=False)
sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER,
                            username TEXT,
                            phone TEXT,
                            addres TEXT,
                            email TEXT,
                            passport TEXT);"""

sql = db.cursor()
sql.execute(sqlite_create_table_query)
db.commit()

load_dotenv('./.env')
token = os.environ.get('TOKEN')

bot = telebot.TeleBot(token)

def get():
    users = sql.execute("SELECT * FROM users").fetchall()
    print(users)


@bot.message_handler(commands=["start"])
def send_mess(message):
    user_ID = message.from_user.id
    username = message.from_user.username
    data = {
    "telegram_id": user_ID,
    "username": username
}
    requests.post('http://165.232.152.194/api/started/', data=data)
    sql.execute(f"SELECT id FROM users WHERE id = {user_ID}")
    if sql.fetchone() is None:
        sql.execute(
            f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
            (user_ID, username, None, None, None, None),
        )
        db.commit()

    bot.send_message(
        message.chat.id, start_text,
        reply_markup=start_keyboard,
    )
    get()

@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == create_card:
        bot.send_message(
            message.chat.id, open_card_text,
            reply_markup=CreateCardRequestKeyboard
        )
    elif message.text == create_questions:
        bot.send_message(
            message.chat.id, question_text,
            reply_markup=QuestionKeyboard
        )
    elif message.text == sample_power_of_attorney:
        bot.send_message(
            message.chat.id, sample_text,
        )
        f = open("./образец_доверенности_без_перс_данныхВ1_2.pdf","rb")
        bot.send_document(
            message.chat.id, f, reply_markup=SampeKeyboard
        )
    elif message.text == open_ooo:
        bot.send_message(
            message.chat.id, open_ooo_text,
            reply_markup=OooKeyboard
        )
    elif message.text == see_ofert:
        f = open("./Оферта_2.0.pdf","rb")
        bot.send_document(
            message.chat.id, f,
            reply_markup=MainPageKeyBoard
        )
    elif message.text == ask_question:
        bot.send_message(
            message.chat.id, ask_question_text,
            reply_markup=MainPageKeyBoard
        )

    elif message.text == pay_button:
        bot.send_message(
            message.chat.id,
            f"Общая стоимость оформления карты 19990 руб.\n\n\
            Ссылка для предоплаты:\n\
            {prepayment()},\n\n\
            Остаток оплаты при получении карты(16990 руб.)\n\
            {pay()}"
        )
    elif message.text == phone_number:
        phone_num = bot.send_message(
            message.chat.id, 'Введите номер телефона для связи'
        )


bot.register_next_step_handler(phone_num, get_num)

    elif message.text == load_adress:
        addr = bot.send_message(
            message.chat.id, 'Введите ваш адресс'
        )
        bot.register_next_step_handler(addr, get_addr)

    elif message.text == tarif_button:
        bot.send_message(
            message.chat.id, tarif
        )
    elif message.text == load_email:
        em = bot.send_message(
            message.chat.id, 'Введите ваш email'
        )
        bot.register_next_step_handler(em, get_em)


def get_em(message):
    message_to_save = message.text
    user_ID = message.from_user.id
    sql.execute(f"UPDATE users SET email = '{message_to_save}' WHERE id = {user_ID}")
    db.commit()
    bot.send_message(
        message.chat.id, "email успешно сохранен",
        reply_markup=loadPhoneKeyboard
    )


def get_num(message):
    message_to_save = message.text
    user_ID = message.from_user.id
    sql.execute(f"UPDATE users SET phone = '{message_to_save}' WHERE id = {user_ID}")
    db.commit()
    bot.send_message(
        message.chat.id, "Номер успешно сохранен",
        reply_markup=start_keyboard
    )

    user_ID = message.from_user.id
    user = sql.execute(f"SELECT * from users WHERE id = {user_ID}").fetchone()
    print(user)
    send_to_db(user[0], user[1], user[2], user[3], user[4], user[5])
    chat_id = 5270959701
    if user[4]:
        f = open(user[5],"rb")
        bot.send_document(
            chat_id, f
        )
        bot.send_message(
            chat_id, f"{user[2]}\n\n{user[3]}\n\n{user[4]}"
        )
    else:
        bot.send_message(
            chat_id, f"{user[2]}\n\n{user[3]}\n\n{user[4]}"
        )
    bot.send_message(
        message.chat.id, "Данные были успешно отправленны на модерацию"
    )
    get()

def get_addr(message):
    message_to_save = message.text
    user_ID = message.from_user.id
    sql.execute(f"UPDATE users SET addres = '{message_to_save}' WHERE id = {user_ID}")
    db.commit()
    bot.send_message(
        message.chat.id, "Адрес успешно сохранен", reply_markup=loadEmailKeyboard
    )
    get()


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == create_request:
        bot.send_message(
            call.message.chat.id, request_text

        )
        f = open("./passport.png","rb")
        bot.send_photo(
            call.message.chat.id, f,
            reply_markup=RequestLoadKeyboard
        )
    elif call.data == 'what':
        bot.send_message(
            call.message.chat.id, wath_easy_vise,
            reply_markup=MainPageKeyBoard
        )
    elif call.data == main_page:
        bot.send_message(
            call.message.chat.id, start_text,
            reply_markup=start_keyboard,
        )
    elif call.data == sample_power_of_attorney:
        bot.send_message(
            call.message.chat.id, sample_text,
        )
        f = open("./образец_доверенности_без_перс_данныхВ1_2.pdf","rb")
        bot.send_document(
            call.message.chat.id, f, reply_markup=SampeKeyboard
        )
    elif call.data == create_ooo_request:
        bot.send_message(
            call.message.chat.id, ooo_text,
            reply_markup=MainPageKeyBoard
        )
    elif call.data == ok_load:
        bot.send_message(
            call.message.chat.id, 'Загрузите фото в хорошем качестве без бликов',
        )

    elif call.data == how_create_card:
        bot.send_message(
            call.message.chat.id, how_create_card_text,
            reply_markup=HowCreateCardKeyboard
        )
    elif call.data == bank_open_bill:
        bot.send_message(
            call.message.chat.id, bank_open_bill_text,
            reply_markup=MainPageKeyBoard
        )
    elif call.data == debet_bill:
        bot.send_message(
            call.message.chat.id, debet_bill_text,
            reply_markup=MainPageKeyBoard
        )
    elif call.data == warranty:
        bot.send_message(
            call.message.chat.id, warranty_text,

Mikasa Ackerman, [6/7/22 2:57 PM]
reply_markup=MainPageKeyBoard
        )
    elif call.data == currency_bill:
        bot.send_message(
            call.message.chat.id, currency_bill_text,
            reply_markup=MainPageKeyBoard
        )
    elif call.data == ofert:
        bot.send_message(
            call.message.chat.id, ofert_text
        )
        f = open("./Оферта_2.0.pdf","rb")
        bot.send_document(
            call.message.chat.id, f,
            reply_markup=MainPageKeyBoard
        )

@bot.message_handler(func=lambda m: True, content_types=["photo"])
def get_documents(message):
    username = message.from_user.username
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)


    dir = os.path.join("documents")
    if not os.path.exists(dir):
        os.mkdir(dir)


    with open(f"./documents/passport_{username}.jpeg", 'wb') as new_file:
        new_file.write(downloaded_file)
    user_ID = message.from_user.id
    sql.execute(f"UPDATE users SET passport = './documents/passport_{username}.jpeg' WHERE id = {user_ID}")
    db.commit()

    bot.send_message(
        message.chat.id, "Фото паспорта было успешно принято в обработку",
        reply_markup=loadAddressKeyboard
    )

@bot.message_handler(func=lambda m: True, content_types=["document"])
def get_documents_file(message):
    username = message.from_user.id
    file_name = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)

    dir = os.path.join("documents")
    if not os.path.exists(dir):
        os.mkdir(dir)


    with open(f"./documents/passport_{username}.jpeg", 'wb') as new_file:
        new_file.write(downloaded_file)
    user_ID = message.from_user.id
    sql.execute(f"UPDATE users SET passport = './documents/passport_{username}.jpeg' WHERE id = {user_ID}")
    db.commit()

    bot.send_message(
        message.chat.id, "Фото паспорта было успешно принято в обработку",
        reply_markup=loadAddressKeyboard
    )



if name == "__main__":
    bot.polling(none_stop=True)