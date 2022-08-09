from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

data_to_text = {
    'france': 'Франция',
    'spain': 'Испания',
    'finland': 'Финляндия',
    'moscow': 'Москва',
    'spb': 'Питер',
    'lonely': 'Один',
    'family': 'Группа (семья)',
    'add_one': 'Добавить заявителя',
    'add_all': 'Я добавил всех заявителей',
    'priority': 'Приоритет',
    'standard': 'Стандарт'
}

markup_empty = InlineKeyboardMarkup(row_width=2)


markup_chose_country = InlineKeyboardMarkup(row_width=2)
markup_chose_country.add(*[
    InlineKeyboardButton(text="Франция", callback_data='france'),
    InlineKeyboardButton(text="Испания", callback_data='spain'),
    InlineKeyboardButton(text="Финляндия", callback_data='finland')])


markup_chose_city = InlineKeyboardMarkup(row_width=2)
markup_chose_city.add(*[
    InlineKeyboardButton(text="Москва", callback_data='moscow'),
    InlineKeyboardButton(text="Питер", callback_data='spb')])


markup_france_chose_family = InlineKeyboardMarkup(row_width=2)
markup_france_chose_family.add(*[
    InlineKeyboardButton(text="Один", callback_data='lonely'),
    InlineKeyboardButton(text="Группа (семья)", callback_data='family')])


markup_add = InlineKeyboardMarkup(row_width=2)
markup_add.add(*[
    InlineKeyboardButton(text="Добавить заявителя", callback_data='add_one'),
    InlineKeyboardButton(text="Я добавил всех заявителей", callback_data='add_all')])


markup_chose_priority = InlineKeyboardMarkup(row_width=2)
markup_chose_priority.add(*[
    InlineKeyboardButton(text="Приоритет", callback_data='priority'),
    InlineKeyboardButton(text="Стандарт", callback_data='standard')])



