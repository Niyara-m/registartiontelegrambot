from telebot import types

def phone_number_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    phone = types.KeyboardButton('Отправить номер', request_contact=True)

    kb.add(phone)
    return kb

def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    location = types.KeyboardButton('Отправить геопозицию', request_location=True)

    kb.add(location)
    return kb

def remove():
    types.ReplyKeyboardRemove()
