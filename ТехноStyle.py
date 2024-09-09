import telebot
import buttons
import database

bot = telebot.TeleBot('7192801910:AAFOWy7l86zm7owaJSVLx6-HDV_tpw4o7o0')

@bot.message_handler(commands=['start'])
def start_message(message):
    user = database.check_user(message.from_user.id)
    if user:
        bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=buttons.main_menu_buttons())
    else:
        bot.send_message(message.from_user.id, 'Отправка номера телефона с помощью кнопки', reply_markup=buttons.share_contact_button())

@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id == 1309265817:
        bot.send_message(message.from_user.id, ' Вы вошли в админ панель', reply_markup=buttons.admin_menu_buttons()),
        bot.register_next_step_handler(message, get_action_from_admin)

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    phone_number = message.contact.phone_number
    first_name = message.contact.first_name
    database.register_user(first_name, phone_number, message.from_user.id)
    bot.send_message(message.from_user.id, 'Вы успешно зарегистрировались', reply_markup=buttons.main_menu_buttons())

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    if call.data == 'Catalog':
        bot.send_message(call.message.chat.id, "Список товаров:")
    elif call.data == 'Basket':
        show_basket(call.message.chat.id)
    elif call.data == 'Contacts':
        bot.send_message(call.message.chat.id, "Ваш контакт:")
    elif call.data == 'Settings':
        bot.send_message(call.message.chat.id, "Настройки:")

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == 'Оставить отзыв':
        bot.send_message(message.from_user.id, 'Ждите ваш отзыв...', reply_markup=buttons.back_button())
        bot.register_next_step_handler(message, get_feedback)
    elif message.text == 'Мои заказы':
        data = database.select_user_orders(message.from_user.id)
        if data:
            bot.send_message(message.from_user.id, 'Пару секунд...')
            text = ''
            for i in data:
                text += f'Ваши заказы:\n\nНомер телефона: {i[2]}\nТовар: {i[3]}\nЛокация: {i[4]}\nОбщая стоимость: {i[5]}\n\n'
            bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, 'У вас пока нет заказов')

    elif message.text == 'Заказать товар':
        bot.send_message(message.from_user.id, 'Выберите товар:  ', reply_markup=buttons.product_name_buttons())
        bot.register_next_step_handler(message, get_product_to_order)


def get_product_to_order(message):
    product_name = message.text

    data = database.select_current_product_by_name(product_name)
    
    bot.send_photo(message.from_user.id, data[3], caption=f'{product_name}n\nОписание: {data[2]}\n\nЦена: {data[-1]}')
    bot.send_message(message.from_user.id, 'Добавить корзину')

    bot.register_next_step_handler(message, get_product_amount, product_name)



def get_product_amount(message, product_name):
    bot.send_message(message.from_user.id, 'Введите кол-во', reply_markup=buttons.amount_buttons())
    bot.register_next_step_handler(message, get_amount, product_name)



def get_amount(message, product_name, product_price):
    product_amount = int(message.text)

    data = database.select_current_product_by_name(product_name)

    if data:
        total_price = data[-1] * product_amount

        database.add_product_to_basket(message.from_user.id, product_amount, product_price)

        bot.send_message(message.from_user.id, 'Продукт добавлен в корзину', reply_markup=buttons.product_name_buttons())

    else:
        bot.send_message(message.from_user.id, 'Что то пошло не так...')


    bot.send_message(message.from_user.id, 'Продукт добавлен в корзину ', reply_markup= buttons.product_name_buttons())







def get_feedback(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в меню', reply_markup=buttons.main_menu_buttons())
    elif message.text == 'Удалить отзыв':
        bot.send_message(message.from_user.id, 'Отзыв удален', reply_markup=buttons.main_menu_buttons())
    else:
        telegram_id = message.from_user.id
        user_feedback = message.text
        database.add_feedback(telegram_id, user_feedback)
        bot.send_message(telegram_id, 'Благодарю за отзыв!', reply_markup=buttons.main_menu_buttons())
        bot.send_message(1309265817, 'Новый отзыв:\n' + message.text)

def show_basket(user_id):
    basket = database.get_user_basket(user_id)
    if basket:
        text = 'Ваша корзина:\n'
        for item in basket:
            text += f'ID корзины: {item[0]}, Название продукта: {item[2]}, Количество: {item[4]}, Общая стоимость: {item[5]}, Локация: {item[5]}\n'
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, 'Ваша корзина пуста.')

def get_action_from_admin(message):
    if message.text == 'Добавить товар':
        bot.send_message(message.from_user.id, 'Отправьте название продукта...')
        bot.register_next_step_handler(message, get_product_name)
    elif message.text == 'Удалить товар':
        bot.send_message(message.from_user.id, 'Отправьте название продукта...')
        bot.register_next_step_handler(message, get_product_to_delete)

def get_product_to_delete(message):
    product_to_delete = message.text
    database.delete_product(product_to_delete)
    bot.send_message(message.from_user.id, 'Вы успешно удалили продукт', reply_markup=buttons.admin_menu_buttons())

def get_product_name(message):
    product_name = message.text
    bot.send_message(message.from_user.id, f'Отправьте описание товара: {product_name}')
    bot.register_next_step_handler(message, get_product_desc, product_name)

def get_product_desc(message, product_name):
    product_desc = message.text
    bot.send_message(message.from_user.id, f'Отправьте фотографию {product_name}')
    bot.register_next_step_handler(message, get_product_photo, product_name, product_desc)

def get_product_photo(message, product_name, product_desc):
    if message.photo:
        product_photo = message.photo[-1].file_id
        bot.send_message(message.from_user.id, f'Отправьте цену {product_name}')
        bot.register_next_step_handler(message, get_product_price, product_name, product_desc, product_photo)
    else:
        bot.send_message(message.from_user.id, 'Отправьте фото...')
        bot.register_next_step_handler(message, get_product_photo, product_name, product_desc)

def get_product_price(message, product_name, product_desc, product_photo):
    product_price = float(message.text)
    database.add_product(product_name, product_desc, product_photo, product_price)
    bot.send_message(message.from_user.id, 'Вы успешно добавили товар', reply_markup=buttons.admin_menu_buttons())
    bot.register_next_step_handler(message, get_action_from_admin)

bot.polling()
