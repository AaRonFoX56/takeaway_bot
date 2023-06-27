from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import RegisterStates
from config import BOT_TOKEN
from service import set_default_commands
from auth_kb import share_phone_keyboard
from db import add_user_phone, create_user_with_name_and_tg_id
from parser import text, pictures

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# default startup function
async def on_startup(dispatcher):
    # set default commands
    await set_default_commands(dispatcher)


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await RegisterStates.Start.set()
    await message.answer(f"Hello, {message.from_user.full_name}. To order food, you have to register. "
                         f"To proceed, enter your name.")


@dp.message_handler(state=RegisterStates.Start)
async def get_username_and_id(message: types.Message):
    await RegisterStates.SharedName.set()
    create_user_with_name_and_tg_id(message.text, message.chat.id, message)
    print(message.text, ' - is user\'s text')
    print(message.chat.id, ' - is user\'s chat id')
    await message.answer(text="Share your phone number", reply_markup=share_phone_keyboard)


@dp.message_handler(state=RegisterStates.SharedName, content_types=types.ContentTypes.CONTACT)
async def get_user_phone_number(message: types.Message):
    add_user_phone(message.contact, message.chat.id)
    await RegisterStates.Authorised.set()
    print(message.contact.phone_number)
    await message.answer(text="Congratulations, you are registered user.")


@dp.message_handler(state=RegisterStates.all_states, commands='clear')
async def clear_state(message: types.Message):
    await RegisterStates.reset_state()
    await message.answer(text='State has been reset')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


