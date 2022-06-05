import telebot
from config import TOKEN, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Я могу конвертировать валюты: \n- Показать список валют через команду /values \n- Вывести конвертацию ' \
           'валюты через команду <имя валюты> <в какую валюту перевести> '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Введите параметры')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Перевожу {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
