from config import TOKEN

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    print(message)
    username = message.from_user.username
    await bot.send_message(message.from_user.id, f"Здравствуйте, {username}!")


class AddGroup(StatesGroup):
    waiting_for_group = State()


async def group_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Отмена')
    await bot.send_message(text="Введите ссылку на группу:", chat_id=message.chat.id, reply_markup=keyboard)
    await AddGroup.waiting_for_group.set()


async def group_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.finish()
        await message.answer("Действие отменено", reply_markup=markup_menu)
        return
    if "http" not in message.text.lower():
        await bot.send_message(message.from_user.id, "Формат введеных данных не верен\nВведите"
                                                     " ссылку на группу повторно")
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id)
        return


def register_handlers_add_group(dp: Dispatcher):
    dp.register_message_handler(group_start, Text(equals="Добавить группу", ignore_case=True), state="*")
    dp.register_message_handler(group_start, commands="add_group", state="*")
    dp.register_message_handler(group_chosen, state=AddGroup.waiting_for_group)


class DeleteGroup(StatesGroup):
    waiting_for_delete_group = State()


async def delete_group_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = []
    if moders[message.from_user.id].api.target_group:
        for chat in moders[message.from_user.id].api.target_group:
            buttons.append(chat.title)
        keyboard.row(*buttons).add('Отмена')
        await bot.send_message(text="Нажмите на группу, которую хотите удалить:",
                               chat_id=message.chat.id, reply_markup=keyboard)
        await DeleteGroup.waiting_for_delete_group.set()
    else:
        msg = "Вы пока что не отслеживаете сообщества, исправьте это нажав кнопку \"Добавить группу\" в меню!"
        await bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=markup_menu)


async def delete_group_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.finish()
        await message.answer("Действие отменено", reply_markup=markup_menu)
        return
    try:
        chat_to_delete = message.text
        url = ''
        for chat in moders[message.from_user.id].api.target_group:
            if chat.title.lower() == chat_to_delete.lower():
                url = 'https://t.me/' + chat.username
                chat_to_delete = chat
                break
        delete = delete_group_from_base(url)
        if delete:
            await bot.send_message(message.from_user.id, "Группа удалена", reply_markup=markup_menu)
            moders[message.from_user.id].api.target_group.remove(chat_to_delete)
            await state.finish()
            await moders[message.from_user.id].main_sender()
    except:
        print(traceback.format_exc())
        await bot.send_message(message.from_user.id, "Пожалуйста, выберите одну из кнопок")
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id)
        return


def register_handlers_delete_group(dp: Dispatcher):
    dp.register_message_handler(delete_group_start, Text(equals="Удалить группу", ignore_case=True), state="*")
    dp.register_message_handler(delete_group_start, commands="delete_group", state="*")
    dp.register_message_handler(delete_group_chosen, state=DeleteGroup.waiting_for_delete_group)


if __name__ == "__main__":
    register_handlers_add_group(dp)
    register_handlers_delete_group(dp)
    executor.start_polling(dp)