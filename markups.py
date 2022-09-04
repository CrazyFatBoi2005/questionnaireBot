from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

france_cities = {
    'msc': "Москва",
    'spb': "Санкт-Петербург",
    'irk': "Иркутск",
    'kaz': "Казань",
    'kal': "Калининград",
    'hab': "Хабаровск",
    'krasnodar': "Краснодар",
    'krasnoyarsk': "Красноярск",
    'nizh_nov': "Нижний Новгород",
    'novosib': "Новосибирск",
    'omsk': "Омск",
    'perm': "Пермь",
    'rost_on_don': "Ростов-на-Дону",
    'samara': "Самара",
    'saratov': "Саратов",
    'ufa': "Уфа",
    'vlad': "Владивосток",
    'ekat': "Екатеринбург",
}

spain_cities = {
    'msc': "Москва",
    'spb': "Санкт-Петербург",
    'ekat': "Екатеринбург",
    'kaz': "Казань",
    'rost_on_don': "Ростов-на-Дону",
    'novosib': "Новосибирск",
    'nizh_nov': "Нижний Новгород",
    'samara': "Самара",
}

finland_cities = {
    'msc': "Москва",
    'spb': "Санкт-Петербург",
    'arkhan': "Архангельск",
    'vel_nov': "Великий Новгород",
    'vlad': "Владивосток",
    'vologda': "Вологда",
    'viborg': "Выборг",
    'ekat': "Екатеринбург",
    'irk': "Иркутск",
    'kaz': "Казань",
    'kal': "Калининград",
    'krasnodar': "Краснодар",
    'krasnoyarsk': "Красноярск",
    'mur': "Мурманск",
    'nizh_nov': "Нижний Новгород",
    'novosib': "Новосибирск",
    'omsk': "Омск",
    'perm': "Пермь",
    'petrozav': "Петрозаводск",
    'pskov': "Псков",
    'rost_on_don': "Ростов-на-Дону",
    'samara': "Самара",
    'ufa': "Уфа",
}

data_to_text = {
    'france': 'Франция',
    'spain': 'Испания',
    'finland': 'Финляндия',
    'lonely': 'Один',
    'family': 'Группа (семья)',
    'add_one': 'Добавить заявителя',
    'add_all': 'Я добавил всех заявителей',
    'priority': 'Приоритет',
    'standard': 'Стандарт',
    'chose_date': 'Исключить даты',
    'all_date': 'Любая дата',
    'short_stay': 'Обычная подача (Short Stay)',
    'holders': 'Продление (Holders of a 2-5 years visa)',
    'long': 'Длительные визы (Long)',
    'msc': "Москва",
    'irk': "Иркутск",
    'kaz': "Казань",
    'kal': "Калининград",
    'hab': "Хабаровск",
    'krasnodar': "Краснодар",
    'krasnoyarsk': "Красноярск",
    'nizh_nov': "Нижний Новгород",
    'novosib': "Новосибирск",
    'omsk': "Омск",
    'perm': "Пермь",
    'rost_on_don': "Ростов-на-Дону",
    'spb': "Санкт-Петербург",
    'samara': "Самара",
    'saratov': "Саратов",
    'ufa': "Уфа",
    'vlad': "Владивосток",
    'ekat': "Екатеринбург",
    'arkhan': "Архангельск",
    'vel_nov': "Великий Новгород",
    'vologda': "Вологда",
    'viborg': "Выборг",
    'mur': "Мурманск",
    'petrozav': "Петрозаводск",
    'pskov': "Псков",
    'all_right': "Всё верно",
    'restart': "Перезапуск",
    'new_message': "Добавить заявителя на запись",
    'change': "Внести изменения в бота",
}

markup_menu = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
markup_menu.add(*[
    InlineKeyboardButton(text="Добавить заявителя на запись", callback_data='new_message'),
    InlineKeyboardButton(text="Внести изменения в бота", callback_data='change')])


markup_empty = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)


markup_check_change = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_check_change.add(*[
    InlineKeyboardButton(text="Всё верно", callback_data='all_right'),
    InlineKeyboardButton(text="Заполнить заново", callback_data='restart')])


markup_chose_country = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_chose_country.add(*[
    InlineKeyboardButton(text="Франция", callback_data='france'),
    InlineKeyboardButton(text="Испания", callback_data='spain'),
    InlineKeyboardButton(text="Финляндия", callback_data='finland')])


markup_chose_france_city = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
cities = []
for key in france_cities.keys():
    cities.append(InlineKeyboardButton(text=france_cities[key], callback_data=key))
markup_chose_france_city.add(*cities)


markup_chose_spain_city = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
cities = []
for key in spain_cities.keys():
    cities.append(InlineKeyboardButton(text=spain_cities[key], callback_data=key))
markup_chose_spain_city.add(*cities)


markup_chose_finland_city = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
cities = []
for key in finland_cities.keys():
    cities.append(InlineKeyboardButton(text=finland_cities[key], callback_data=key))
markup_chose_finland_city.add(*cities)


markup_france_chose_family = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_france_chose_family.add(*[
    InlineKeyboardButton(text="Один", callback_data='lonely'),
    InlineKeyboardButton(text="Группа (семья)", callback_data='family')])


markup_add = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_add.add(*[
    InlineKeyboardButton(text="Добавить заявителя", callback_data='add_one'),
    InlineKeyboardButton(text="Я добавил всех заявителей", callback_data='add_all')])


markup_chose_priority = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_chose_priority.add(*[
    InlineKeyboardButton(text="Приоритет", callback_data='priority'),
    InlineKeyboardButton(text="Стандарт", callback_data='standard')])


markup_need_date = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_need_date.add(*[
    InlineKeyboardButton(text="Любая дата", callback_data='all_date'),
    InlineKeyboardButton(text="Исключить даты", callback_data='chose_date')])


markup_check = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_check.add(*[
    InlineKeyboardButton(text="Всё верно", callback_data='all_right'),
    InlineKeyboardButton(text="Заполнить заново", callback_data='restart')])


markup_category = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
markup_category.add(*[
    InlineKeyboardButton(text="Обычная подача (Short Stay)", callback_data='short_stay'),
    InlineKeyboardButton(text="Продление (Holders of a 2-5 years visa)", callback_data='holders'),
    InlineKeyboardButton(text="Длительные визы (Long)", callback_data='long')])
