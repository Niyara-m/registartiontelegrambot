import telebot, database, buttons
from geopy import Nominatim

bot = telebot.TeleBot('6488024104:AAFrPjMjy2GeKpwOKdMktlU3lw-AkoXWo2A')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')


@bot.message_handler(commands=['start'])

def start_message(message):
    global user_id
    user_id = message.from_user.id
    check_user = database.check_registration(user_id)
    if check_user:
        bot.send_message(user_id, f'{message.from_user.first_name}! Добро пожаловать!', reply_markup=buttons.remove())
    else:
        bot.send_message(user_id, 'Пройдите регистрацию! Введите свое Имя', reply_markup=buttons.remove())
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Отправьте пожалуйста свой номер!', reply_markup=buttons.phone_number_button())
    bot.register_next_step_handler(message, get_phone_number, user_name)

def get_phone_number(message, user_name):
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'А теперь отправьте локацию!',
                         reply_markup=buttons.location_button())
        #Переход на этап получения локации
        bot.register_next_step_handler(message, get_location, user_name, user_num)
    #Если не нажимал кнопку
    else:
        bot.send_message(user_id, 'Отправьте свой контакт через кнопку!')
        bot.register_next_step_handler(message, get_phone_number, user_name)

def get_location(message, user_name, user_num):
    # Если нажал на кнопку
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.longitude},'
                                      f'{message.location.latitude}')
        # Регистрируем пользователя
        database.registration(user_id, user_name, user_num, user_loc)
        # Перевод на главное меню
        bot.send_message(user_id, 'Вы успешно зарегистрировались!')

    # Если не нажал кнопку
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(message, get_location, user_name, user_num)

bot.polling(non_stop=True)