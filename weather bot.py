from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types
import datetime
import pytz
import os, sys

bot = telebot.TeleBot('5871701106:AAHx7qNK9g3SCzpXCXrfy95_LAXTZ9t7vz0')

def weather_check():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    res = requests.get(
        'https://www.google.com/search?q=пермь погода&oq=пермь погода&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    precipitation = soup.select('#wob_dc')[0].getText().strip()
    temp = soup.select('#wob_tm')[0].getText().strip()
    precipitation_probability = soup.select('#wob_pp')[0].getText().strip()
    wind = soup.select('#wob_ws')[0].getText().strip()
    humidity = soup.select('#wob_hm')[0].getText().strip()
    return(precipitation.lower(), temp, wind, humidity, precipitation_probability)

def time_check():
    tz = pytz.timezone('Asia/Yekaterinburg')  # Получение объекта часового пояса для заданного города в формате "Континент/Город"
    now = datetime.datetime.now(tz)  # Получение текущей даты и времени для заданного города

    weekday_ru = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }

    month_ru = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октября',
        11: 'Ноября',
        12: 'Декабря'
    }

    weekday = now.weekday()
    weekday_ru = weekday_ru[weekday]  # Получение названия дня недели на русском языке

    month_number = now.month
    month_ru = month_ru[month_number]  # Получение названия месяца на русском языке

    formatted_date_time = now.strftime('%H:%M')  # Форматирование даты и времени в указанный формат

    return(f"Сегодня {weekday_ru.lower()}, {now.day} {month_ru.lower()} {now.year} года, время: {formatted_date_time}")


@bot.message_handler(commands=['start', 'Start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather = types.KeyboardButton('Какая погода в Перми сегодня?')
    markup.add(weather)

    userfname = message.from_user.first_name
    bot.send_message(message.chat.id, f'Привет, <b>{userfname}</b>! С помошью этого бота ты сможешь узанть погоду в городе Пермь!',
                     parse_mode='html', reply_markup=markup)

@bot.message_handler()
def income(message):
    if message.text == 'Какая погода в Перми сегодня?':
        print(f"погодой интересуется: {message.from_user.first_name} - @{message.from_user.username}")
        mes = bot.send_message(message.chat.id, f'Получаю данные о погоде на момент {time_check()[18::]}\nПожалуйста подождите')
        try:
            bot.edit_message_text(chat_id = message.chat.id, message_id = mes.id, text = f'{time_check()}\nНа улице {weather_check()[0]}\nТемпература: <b>{weather_check()[1]}°C</b>\nСкорость ветра: <b>{weather_check()[2]}</b>\nВлажность воздуха: <b>{weather_check()[3]}</b>\nВероятность осадков равна: <b>{weather_check()[4]}</b>',
                              parse_mode='html')
        except:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mes.id,
                                  text='Простите, но похоже произошел сбой, сечас данные о погоде получить не удалось, попробуйте позднее')
    else:
        bot.send_message(message.from_user.id, "Прости, но я тебя не понимаю.")

if __name__ == '__main__':
    print("Bot start")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except (ConnectionError, ReadTimeout) as e:
        sys.stdout.flush()
        os.execv(sys.argv[0], sys.argv)
    else:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
        print("Bot start, again")