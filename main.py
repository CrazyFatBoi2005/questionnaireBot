from config import TOKEN
from markups import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

ADMIN = "508537898"

data = {}

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class People:
    def __init__(self):
        self.name = ''
        self.passport = ''
        self.dates = ''
        self.phone = ''


class Blank(StatesGroup):
    country = State()
    city = State()
    count = State()
    name = State()
    passport = State()
    dates = State()
    phone = State()
    confrim = State()
    priority = State()


@dp.message_handler(commands=['start'], state=None)
async def start_message(message: types.Message):
    print(message)
    print(message.from_user.id)
    username = message.from_user.username
    data[message.from_user.id] = {
        'country': '',
        'city': '',
        'count': '',
        'peoples': [],
        'priority': '',
    }
    await bot.send_message(message.from_user.id, f"Здравствуйте, {username}!")
    await Blank.country.set()
    await bot.send_message(message.from_user.id, f"Выберите страну:", reply_markup=markup_chose_country)


@dp.callback_query_handler(state=Blank.country)
async def chose_country(query: CallbackQuery, state: FSMContext):
    data[query.from_user.id]['country'] = data_to_text[query.data]
    await Blank.next()
    await query.message.edit_text(f"Выберите город подачи:")
    await query.message.edit_reply_markup(markup_chose_city)


@dp.callback_query_handler(state=Blank.city)
async def chose_city(query: CallbackQuery, state: FSMContext):
    data[query.from_user.id]['city'] = data_to_text[query.data]
    await Blank.next()
    await query.message.edit_text(f"Выберите количество заявителей:")
    await query.message.edit_reply_markup(markup_france_chose_family)


@dp.callback_query_handler(state=Blank.count)
async def chose_count(query: CallbackQuery, state: FSMContext):
    data[query.from_user.id]['count'] = data_to_text[query.data]
    await Blank.next()
    await bot.delete_message(query.from_user.id, query.message.message_id)
    await bot.send_message(query.from_user.id, f"Напишите Имя и Фамилию заявителя на русском:")


@dp.message_handler(state=Blank.name)
async def write_name(message: types.Message, state: FSMContext):
    data[message.from_user.id]['peoples'].append(People())
    data[message.from_user.id]['peoples'][-1].name = message.text
    await Blank.next()
    await bot.send_message(message.from_user.id, 'Загрузите фото паспорта (pdf, jpeg)',
                           reply_markup=InlineKeyboardMarkup())


@dp.message_handler(content_types=['photo', 'document'], state=Blank.passport)
async def send_passport(message: types.Message, state: FSMContext):
    name = data[message.from_user.id]['peoples'][-1].name
    if message.content_type == 'photo':
        await message.photo[-1].download()
        await message.photo[-1].download(destination_file=f"passports/{name}.jpeg")
        data[message.from_user.id]['peoples'][-1].passport = f"passports/{name}.jpeg"
    elif message.content_type == 'document':
        await message.document.download(destination_file=f"passports/{name}.pdf")
        data[message.from_user.id]['peoples'][-1].passport = f"passports/{name}.pdf"
    await Blank.next()
    await bot.send_message(message.from_user.id, 'Введите даты, которые исключить для записи:')


@dp.message_handler(state=Blank.dates)
async def write_dates(message: types.Message, state: FSMContext):
    data[message.from_user.id]['peoples'][-1].dates = message.text
    await Blank.next()
    await bot.send_message(message.from_user.id, 'Введите номер телефона:')


@dp.message_handler(state=Blank.phone)
async def write_phone(message: types.Message, state: FSMContext):
    data[message.from_user.id]['peoples'][-1].phone = message.text
    if data[message.from_user.id]['count'] == 'Один':
        await Blank.priority.set()
        await bot.send_message(message.from_user.id, 'На какую очередь ставить приоритет или стандарт?'
                                                     ' Бот сначала записывает приоритет, если остаются места переходит'
                                                     ' к стандарту', reply_markup=markup_chose_priority)
    else:
        await Blank.next()
        await bot.send_message(message.from_user.id, 'Хотите ли вы добавить еще одного заявителя?',
                               reply_markup=markup_add)


@dp.callback_query_handler(state=Blank.confrim)
async def confriming(query: CallbackQuery, state: FSMContext):
    if query.data == 'add_one':
        await Blank.name.set()
        await bot.delete_message(query.from_user.id, query.message.message_id)
        await bot.send_message(query.from_user.id, f"Напишите Имя и Фамилию заявителя на русском:")
    elif query.data == 'add_all':
        await Blank.next()
        await bot.send_message(query.from_user.id, 'На какую очередь ставить приоритет или стандарт?'
                                                   ' Бот сначала записывает приоритет, если остаются места переходит'
                                                   ' к стандарту', reply_markup=markup_chose_priority)
        await bot.delete_message(query.from_user.id, query.message.message_id)


@dp.callback_query_handler(state=Blank.priority)
async def chose_priority(query: CallbackQuery, state: FSMContext):
    data[query.from_user.id]['priority'] = data_to_text[query.data]
    await state.finish()
    await bot.send_message(query.from_user.id, 'Заявка отправленна!', reply_markup=ReplyKeyboardMarkup())
    await bot.send_message(ADMIN, build_message(query.from_user.id))
    await bot.send_media_group(ADMIN, media=build_media(query.from_user.id))


def build_media(id):
    global data
    media = types.MediaGroup()
    for p in data[id]['peoples']:
        media.attach_photo(types.InputFile(p.passport), p.name)
    return media


def build_message(id):
    global data
    result = ''
    result += f"Страна: {data[id]['country']}\n"
    result += f"Город подачи: {data[id]['city']}\n"
    result += f"{data[id]['count']}\n\n"
    for p in data[id]['peoples']:
        result += f"Фамилия Имя: {p.name}\n"
        result += f"Диапазон дат исключений: {p.dates}\n"
        result += f"Номер телефона: {p.phone}\n\n"
    result += f"Очередь: {data[id]['priority']}"
    return result


if __name__ == "__main__":
    executor.start_polling(dp)
