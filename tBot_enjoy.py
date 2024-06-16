import telebot

bot = telebot.TeleBot("7359683723:AAHVfnQvwvS1-vWEPQZ4e52_pZoaHTcQ7os")


@bot.message_handler(commands=["start", "help"])
def commands(message):
    bot.reply_to(message, "Использованна одна из двух команд")


@bot.message_handler(content_types=["text", "photo", "sticker"])
def content(message):
    if message.text == "привет":
        bot.send_message(message.chat.id, "Ну привет :3")
    if message.photo:
        bot.send_message(message.chat.id, "U so deutiful")
    if message.sticker:
        bot.send_message(message.chat.id, "Крутой стикер")


bot.polling()
