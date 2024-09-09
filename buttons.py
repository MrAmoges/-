from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import database

def main_menu_buttons():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Category')
    btn2 = KeyboardButton('Basket')
    btn3 = KeyboardButton('Contacts')
    btn4 = KeyboardButton('Settings')
    btn5 = KeyboardButton('Feedback')
    btn6 = KeyboardButton('My_orders')

    kb.add(btn1, btn2, btn3, btn4, btn5,btn6)
    return kb

def share_contact_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Share contact', request_contact=True)
    kb.add(btn1)

    return kb

def register_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Register')
    kb.add(btn1)

    return kb



def back_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn = KeyboardButton('Назад')
    kb.add(btn)

    return kb


def feedback_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Назад')
    btn2 = KeyboardButton('Удалить отзыв')
    kb.add(btn1,btn2)

    return kb

def orders_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Мои заказы')
    kb.add(btn1)

    return kb


def admin_menu_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Добавить товар')
    btn2 = KeyboardButton('Удалить товар')

    kb.add(btn1,btn2)
    
    return kb

def count_buttons():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(1,11):
        kb.add(KeyboardButton(str(i)))

    return kb



def basket_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Добавить в корзинку')
    btn2 = KeyboardButton('Назад')

    kb.add(btn1,btn2)
    
    return kb           



def product_name_buttons():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)


    data = database.select_products_name()

    for i in data:
        kb.add(str(i[0]))

    return kb


def amount_buttons():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(1, 11):
        kb.add(str(i))

    return kb