from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = "7359683723:AAHVfnQvwvS1-vWEPQZ4e52_pZoaHTcQ7os"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Салам алейкум, брат!\nЕсть работа для меня?')


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer("Чем могу быть полезен?")

@dp.message()
async def send_echo(message: Message):
    await message.reply("С такими командами я пока что не знаком.\n" 
                        "Попробуйте /start или /help")
     
if __name__ == '__main__':
    dp.run_polling(bot)