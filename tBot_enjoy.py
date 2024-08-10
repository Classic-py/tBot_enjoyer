import random
import requests
import asyncio
import pickle

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

BOT_TOKEN = "PASS"
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

with open('data_id.pkl', 'rb') as file:
    users = pickle.load(file)

def get_random_number() -> int:
    return random.randint(1, 100)

def saved_res():
    with open('data_id.pkl', 'wb') as file:
        pickle.dump(users, file)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
            }
    saved_res()


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n/reset - обнулить' 
        ' статистику\nДавай сыграем?'
    )

@dp.message(Command(commands='stat'))
async def process_help_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

@dp.message(Command(commands='reset'))
async def process_reset_command(message: Message):
    users[message.from_user.id]['total_games'] = 0
    users[message.from_user.id]['wins'] = 0
    await message.answer('Статистика обнулена.') 
    saved_res()

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играли :3'
            'Может сыграем хоть разок?'
        )
    saved_res()

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
        saved_res()
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if users[message.from_user.id]['secret_number'] == int(message.text):
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
            else:
                cat_link = 'Сдесь должен был быть кот'
            await message.answer(
                'Ура!!! Вы угадали число!\n'
                'Ваш приз - котейка :3'
                )
            await message.answer_photo(photo=cat_link)
            await message.answer('Хотите сыграть ещё?')
        elif users[message.from_user.id]['secret_number'] < int(message.text):
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif users[message.from_user.id]['secret_number'] > int(message.text):
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли \n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
        saved_res()
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

if __name__ == '__main__':
    dp.run_polling(bot)