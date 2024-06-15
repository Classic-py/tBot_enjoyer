import telebot

bot = telebot.TeleBot('7359683723:AAHVfnQvwvS1-vWEPQZ4e52_pZoaHTcQ7os')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте, возникли проблемы с техникой?')

bot.polling(none_stop=True)