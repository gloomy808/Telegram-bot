import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введи команду боту в следующем формате: \n<Имя валюты> <в какую валюту перевести> ' \
           '<Количество переводимой валюты>\nУвидеть список всех доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])  # выводим все доступные валюты
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):  # отправка запросов к API
    try:
        values = message.text.split(' ')  # преобразуем сообщение в список
        if len(values) != 3:  # если список не равен 3 элементам
            raise APIException('Слишком много параметров')

        quote, base, amount = values  # присваиваем переменные каждому элементу списка
        total_base = CryptoConverter.get_price(quote.lower(), base.lower(),
                                             amount)  # вызов метода get_price класса CryproConverter
    except APIException as e:   # отлов ошибок пользователя
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:  # отлов ошибок сервера
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'  # подсчет суммы
        bot.send_message(message.chat.id, text)  # передаем сообщение с суммой сконвертируемой валюты

bot.polling(none_stop=True)
