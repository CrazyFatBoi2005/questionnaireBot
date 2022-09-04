import random
import os
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

from sql_commands import *

ADMIN = 508537898
ADMIN2 = 760565355

last_message = {}

user_to_reg = {
    'username': '',
    'name': ''
}
data = {}
changing_data = {}

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
agents = get_usernames()


class People:
    def __init__(self):
        self.name = ''
        self.passport = ''


class Blank(StatesGroup):
    country = State()
    city = State()
    count = State()
    spain_finland_state = State()
    delay = State()
    category = State()
    podcategory = State()
    name = State()
    passport = State()
    confrim = State()
    before_dates = State()
    dates = State()
    phone = State()
    priority = State()
    accept = State()


class Changing(StatesGroup):
    country = State()
    names = State()
    change = State()
    check = State()


@dp.message_handler(commands=['start'], state="*")
async def start_message(message: types.Message,  state: FSMContext):
    data[message.from_user.id] = {
        'country': '',
        'city': '',
        'count': '',
        'delay': '',
        'category': '',
        'podcategory': '',
        'peoples': [],
        'phone': '',
        'dates': '',
        'priority': '',
    }
    changing_data[message.from_user.id] = {}
    await state.finish()
    print(message)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f"Здравствуйте, {username}!")
    last_message[message.from_user.id] = await send_menu(message.from_user.id)
    print(last_message[message.from_user.id])


@dp.message_handler(commands=['change'], state="*")
async def change_message(message: types.Message):
    print('Change\n', message)
    username = message.from_user.username
    if username in agents or message.from_user.id == ADMIN:
        changing_data[message.from_user.id] = {}
        await Changing.country.set()
        last_message[message.from_user.id] = await bot.send_message(message.from_user.id, f"*Выберите страну:*",
                                                                    reply_markup=markup_chose_country,
                                                                    parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, f"Здравствуйте, {username}! Вы не имеете прав для использования"
                                                     f" данной команды, обратитесь к @bavshin_ruslan")


@dp.callback_query_handler(state=Changing.country)
async def choose_country_changing(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    changing_data[query.from_user.id]['country'] = data_to_text[query.data]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    await Changing.next()
    last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                              f"*Напишите на русском Фамилию и Имя заявителя или"
                                                              f" всех заявителей через запятую*",
                                                              parse_mode="Markdown")


@dp.message_handler(state=Changing.names)
async def choose_names_changing(message: types.Message, state: FSMContext):
    changing_data[message.from_user.id]['names'] = message.text
    await Changing.change.set()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                    f"*Введите подробные изменения заявки:*",
                                                                    parse_mode="Markdown")


@dp.message_handler(state=Changing.change)
async def write_change(message: types.Message, state: FSMContext):
    changing_data[message.from_user.id]['change'] = message.text
    user = message.from_user
    await Changing.check.set()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                f"*Проверьте изменения:\n\n*" +
                                                                report_text(changing_data[user.id]),
                                                                reply_markup=markup_check_change,
                                                                parse_mode="Markdown")


@dp.callback_query_handler(state=Changing.check)
async def check_chages(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    if query.data == "all_right":
        await state.finish()
        await bot.send_message(query.from_user.id, f"*ИЗМЕНЕНИЯ ПРИНЯТЫ!*",
                               parse_mode="Markdown")
        last_message[query.from_user.id] = await send_menu(query.from_user.id)
        await bot.send_message(ADMIN, moder_text(user.username) + report_text(changing_data[user.id]),
                               parse_mode="Markdown")
        await bot.send_message(ADMIN2, moder_text(user.username) + report_text(changing_data[user.id]),
                               parse_mode="Markdown")
    elif query.data == "restart":
        msg = last_message[query.from_user.id]
        await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
        await bot.send_message(query.from_user.id, f"*ИЗМЕНЕНИЯ НЕ ПРИНЯТЫ!*",
                               parse_mode="Markdown")
        await bot.send_message(query.from_user.id, f"        ▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️",
                               parse_mode="Markdown")
        changing_data[query.from_user.id] = {}
        await Changing.country.set()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите страну:*",
                                                                  reply_markup=markup_chose_country,
                                                                  parse_mode="Markdown")


class AddUser(StatesGroup):
    username = State()
    name = State()


@dp.message_handler(commands=['adduser'], state="*")
async def add_user(message: types.Message):
    print(message)
    username = message.from_user.username
    if message.from_user.id == ADMIN:
        await AddUser.username.set()
        await bot.send_message(message.from_user.id, f"*Введите username без знака '@':*",
                               parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, f"Здравствуйте, {username}! Вы не имеете прав для использования"
                                                     f" данной команды, обратитесь к @bavshin_ruslan")


@dp.message_handler(state=AddUser.username)
async def write_username(message: types.Message, state: FSMContext):
    user_to_reg['username'] = message.text
    await AddUser.name.set()
    await bot.send_message(message.from_user.id, f"*Введите текстовое имя пользователя:*",
                           parse_mode="Markdown")


@dp.message_handler(state=AddUser.name)
async def write_name_for_user(message: types.Message, state: FSMContext):
    global agents, user_to_reg
    user_to_reg['name'] = message.text
    await state.finish()
    await bot.send_message(message.from_user.id, f"Пользователь {user_to_reg['username']} получил доступ к работе с ботом!",
                           parse_mode="Markdown")
    add_user_to_base([user_to_reg['username'], user_to_reg['name']])
    print(f"Пользователь {user_to_reg['username']} получил доступ к работе с ботом!")
    agents = get_usernames()
    user_to_reg.clear()


@dp.callback_query_handler(state=Blank.country)
async def chose_country(query: CallbackQuery, state: FSMContext):
    data[query.from_user.id] = {
        'country': '',
        'city': '',
        'count': '',
        'delay': '',
        'category': '',
        'podcategory': '',
        'peoples': [],
        'phone': '',
        'dates': '',
        'priority': '',
    }
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    data[query.from_user.id]['country'] = data_to_text[query.data]
    await Blank.next()
    if query.data == 'france':
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите город подачи:*",
                                                                  parse_mode="Markdown",
                               reply_markup=markup_chose_france_city)
    elif query.data == 'spain':
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите город подачи:*",
                                                                  parse_mode="Markdown",
                               reply_markup=markup_chose_spain_city)
    elif query.data == 'finland':
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите город подачи:*",
                                                                  parse_mode="Markdown",
                               reply_markup=markup_chose_finland_city)


@dp.callback_query_handler(state=Blank.city)
async def chose_city(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    data[query.from_user.id]['city'] = data_to_text[query.data]
    await Blank.next()
    last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите количество заявителей:*",
                                                              parse_mode="Markdown",
                                                              reply_markup=markup_france_chose_family)


@dp.callback_query_handler(state=Blank.count)
async def chose_count(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    data[query.from_user.id]['count'] = data_to_text[query.data]
    print(data[query.from_user.id]['country'])
    if data[query.from_user.id]['country'] == data_to_text['france']:
        await Blank.category.set()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id, f"*Выберите категорию записи:*",
                                                                  parse_mode="Markdown", reply_markup=markup_category)
    else:
        await Blank.delay.set()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                  f"*Сколько дней оставлять между записью и подачей?*\n"
                                                                  f"Напишите количество дней от 0",
                                                                  parse_mode="Markdown")


@dp.message_handler(state=Blank.delay)
async def write_delay(message: types.Message, state: FSMContext):
    data[message.from_user.id]['delay'] = message.text
    await Blank.name.set()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                f"*Напишите Имя и Фамилию заявителя на русском:*",
                                                                parse_mode="Markdown")


@dp.callback_query_handler(state=Blank.category)
async def chose_category(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    data[query.from_user.id]['category'] = data_to_text[query.data]
    if query.data == 'long':
        await Blank.next()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                  f'*На какую подкатегорию "Long" записывать?*',
                                                                  parse_mode="Markdown")
    elif query.data == 'short_stay' or query.data == 'holders':
        await Blank.name.set()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                  f"*Напишите Имя и Фамилию заявителя на русском:*",
                                                                  parse_mode="Markdown")


@dp.message_handler(state=Blank.podcategory)
async def write_category(message: types.Message, state: FSMContext):
    data[message.from_user.id]['podcategory'] = message.text
    await Blank.next()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                f"*Напишите Имя и Фамилию заявителя на русском:*",
                                                                parse_mode="Markdown")


@dp.message_handler(state=Blank.name)
async def write_name(message: types.Message, state: FSMContext):
    data[message.from_user.id]['peoples'].append(People())
    data[message.from_user.id]['peoples'][-1].name = message.text
    await Blank.next()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                '*Загрузите фото паспорта (pdf, jpeg):*',
                                                                reply_markup=InlineKeyboardMarkup(),
                                                                parse_mode="Markdown")


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
    if data[message.from_user.id]['count'] == 'Один':
        await Blank.before_dates.set()
        last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                    '*Записываем на любые даты подачи?*',
                                                                    reply_markup=markup_need_date,
                                                                    parse_mode="Markdown")
    elif data[message.from_user.id]['count'] == 'Группа (семья)':
        await Blank.confrim.set()
        last_message[message.from_user.id] = \
            await bot.send_message(message.from_user.id, '*Хотите ли вы добавить еще одного заявителя?*',
                                   reply_markup=markup_add, parse_mode="Markdown")


@dp.callback_query_handler(state=Blank.before_dates)
async def before_dates(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    if query.data == 'chose_date':
        await Blank.next()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                  '*Введите даты или диапазон дат,'
                                                                  ' которые исключить для записи:*',
                                                                  parse_mode="Markdown")
    elif query.data == 'all_date':
        data[query.from_user.id]['dates'] = data_to_text[query.data]
        await Blank.phone.set()
        last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                  '*Введите номер телефона:*',
                                                                  parse_mode="Markdown")


@dp.message_handler(state=Blank.dates)
async def write_dates(message: types.Message, state: FSMContext):
    data[message.from_user.id]['dates'] = message.text
    await Blank.next()
    last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                '*Введите номер телефона:*',
                                                                parse_mode="Markdown")


@dp.message_handler(state=Blank.phone)
async def write_phone(message: types.Message, state: FSMContext):
    data[message.from_user.id]['phone'] = message.text
    if data[message.from_user.id]['country'] == data_to_text['france']:
        await Blank.priority.set()
        last_message[message.from_user.id] = await bot.send_message(message.from_user.id,
                                                                    '*На какую очередь ставить приоритет'
                                                                    ' или стандарт?*\n'
                                                                    'Бот сначала записывает приоритет,'
                                                                    ' если остаются места переходит к стандарту',
                                                                    parse_mode="Markdown",
                                                                    reply_markup=markup_chose_priority)
    else:
        await Blank.accept.set()
        last_message[message.from_user.id] =\
            await bot.send_message(message.from_user.id,
                                   '*Пожалуйста, проверьте вашу заявку:*\n\n' + build_message(message.from_user.id),
                                   reply_markup=markup_check,
                                   parse_mode="Markdown")


@dp.callback_query_handler(state=Blank.confrim)
async def confriming(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    if query.data == 'add_one':
        await Blank.name.set()
        last_message[query.from_user.id] =\
            await bot.send_message(query.from_user.id, f"*Напишите Имя и Фамилию заявителя на русском:*",
                                   parse_mode="Markdown")
    elif query.data == 'add_all':
        if data[query.from_user.id]['country'] == data_to_text['france']:
            await Blank.before_dates.set()
            last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                      '*Записываем на любые даты подачи?*',
                                                                      reply_markup=markup_need_date,
                                                                      parse_mode="Markdown")
            """last_message[query.from_user.id] =\
                await bot.send_message(query.from_user.id, '*На какую очередь ставить приоритет или стандарт*\n'
                                                           'Бот сначала записывает приоритет,'
                                                           ' если остаются места переходит к стандарту',
                                       parse_mode="Markdown", reply_markup=markup_chose_priority)"""
        else:
            await Blank.before_dates.set()
            last_message[query.from_user.id] = await bot.send_message(query.from_user.id,
                                                                      '*Записываем на любые даты подачи?*',
                                                                      reply_markup=markup_need_date,
                                                                      parse_mode="Markdown")
            """last_message[query.from_user.id] = \
                await bot.send_message(query.from_user.id,
                                       '*Пожалуйста, проверьте вашу заявку:*\n' + build_message(query.from_user.id),
                                       reply_markup=markup_check,
                                       parse_mode="Markdown")"""


@dp.callback_query_handler(state=Blank.priority)
async def chose_priority(query: CallbackQuery, state: FSMContext):
    msg = last_message[query.from_user.id]
    await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    data[query.from_user.id]['priority'] = data_to_text[query.data]
    await Blank.next()
    last_message[query.from_user.id] = \
        await bot.send_message(query.from_user.id,
                               '*Пожалуйста, проверьте вашу заявку:*\n\n' + build_message(query.from_user.id),
                               reply_markup=markup_check,
                               parse_mode="Markdown")


@dp.callback_query_handler(state=Blank.accept)
async def accepting(query: CallbackQuery, state: FSMContext):
    if query.data == 'all_right':
        await state.finish()
        await bot.send_message(query.from_user.id, '*ЗАЯВКА ОТПРАВЛЕНА!*', reply_markup=InlineKeyboardMarkup(),
                               parse_mode="Markdown")
        last_message[query.from_user.id] = await send_menu(query.from_user.id)
        await bot.send_message(ADMIN, moder_text(query.from_user.username) + build_message(query.from_user.id),
                               parse_mode="Markdown")
        await bot.send_media_group(ADMIN, media=build_media(query.from_user.id))
        await bot.send_message(ADMIN2, moder_text(query.from_user.username) + build_message(query.from_user.id),
                               parse_mode="Markdown")
        await bot.send_media_group(ADMIN2, media=build_media(query.from_user.id))
    elif query.data == 'restart':
        msg = last_message[query.from_user.id]
        await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
        await bot.send_message(query.from_user.id, '*ЗАЯВКА НЕ ОТПРАВЛЕНА!*', reply_markup=InlineKeyboardMarkup(),
                               parse_mode="Markdown")
        await bot.send_message(query.from_user.id, f"        ▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️",
                               parse_mode="Markdown")
        await Blank.country.set()
        last_message[query.from_user.id] =\
            await bot.send_message(query.from_user.id, f"*Выберите страну:*", reply_markup=markup_chose_country,
                                   parse_mode="Markdown")


def build_media(id):
    global data
    media = types.MediaGroup()
    for p in data[id]['peoples']:
        file = types.InputFile(p.passport)
        filename, file_extension = os.path.splitext(p.passport)
        if file_extension == 'pdf':
            media.attach_document(file, p.name)
        else:
            media.attach_photo(file, p.name)
    return media


def build_message(id):
    global data
    result = f"*Страна:* {data[id]['country']}\n"
    result += f"*Город подачи:* {data[id]['city']}\n"
    result += f"*Количество заявителей:* {data[id]['count']} - {len(data[id]['peoples'])}\n"
    result += f"*Диапазон дат исключений:* {data[id]['dates']}\n"
    result += f"*Номер телефона:* {data[id]['phone']}\n"
    if data[id]['country'] == data_to_text['france']:
        result += f"*Категория:* {data[id]['category']}\n"
        if data[id]['podcategory'] != '':
            result += f"*Подкатегория:* {data[id]['podcategory']}\n"
        result += f"*Очередь:* {data[id]['priority']}\n"
    else:
        result += f"*Сколько дней оставлять между записью и подачей:* {data[id]['delay']}\n"
    result += "\n"
    i = 1
    for p in data[id]['peoples']:
        result += f"*{i})*\n"
        result += f"*Фамилия Имя:* {p.name}\n"
        i += 1
    return result


def moder_text(username):
    return f"{username}\n{get_name(username)[0]}\n\n"


def report_text(dict_: dict):
    result = f"*Страна:* {dict_['country']}\n"
    result += f"*Фамилии и Имена:* {dict_['names']}\n"
    result += f"*Изменения в заявке:* {dict_['change']}"
    return result


async def send_menu(id):
    await bot.send_message(id, f"        ▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️",
                           parse_mode="Markdown")
    return await bot.send_message(id, "*Выберите опцию:*", reply_markup=markup_menu, parse_mode="Markdown")


@dp.callback_query_handler()
async def menu_holder(query: CallbackQuery):
    try:
        msg = last_message[query.from_user.id]
        await bot.edit_message_text(data_to_text[query.data], query.from_user.id, msg.message_id)
    except KeyError:
        print('no last_message')
    if query.data == "new_message":
        username = query.from_user.username
        if username in agents or query.from_user.id == ADMIN:
            await Blank.country.set()
            last_message[query.from_user.id] =\
                await bot.send_message(query.from_user.id, f"*Выберите страну:*", reply_markup=markup_chose_country,
                                       parse_mode="Markdown")
        else:
            await bot.send_message(query.from_user.id,
                                   f"*Обратитесь к @bavshin_ruslan, чтобы вас добавили в систему*",
                                   parse_mode="Markdown")
    elif query.data == "change":
        print('Change\n', query)
        username = query.from_user.username
        changing_data[query.from_user.id] = {}
        if username in agents or query.from_user.id == ADMIN:
            await Changing.country.set()
            last_message[query.from_user.id] = \
                await bot.send_message(query.from_user.id, f"*Выберите страну:*", reply_markup=markup_chose_country,
                                       parse_mode="Markdown")
        else:
            await bot.send_message(query.from_user.id,
                                   f"Здравствуйте, {username}! Вы не имеете прав для использования"
                                   f" данной команды, обратитесь к @bavshin_ruslan")

if __name__ == "__main__":
    executor.start_polling(dp)
