from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import States
import phrasebook
import kinopoisk
import keyboards
import logging
import typing as tp
from config import BOT_TOKEN
from database import DataBase

database = DataBase()

logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=BOT_TOKEN,
)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)


async def remove_last_inline(last_message: types.Message, state: FSMContext) -> None:
    idx = last_message.message_id - 1
    data = await state.get_data()
    if 'Not_delete' in data and data['Not_delete']:
        await state.update_data(Not_delete=False)
        return
    try:
        await bot.edit_message_reply_markup(last_message.chat.id, idx, reply_markup=None)
    except Exception:
        pass


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext) -> None:
    await remove_last_inline(message, state)
    types.ReplyKeyboardRemove()
    await message.answer(phrasebook.WELCOME)


@dp.message_handler(commands=['help'], state='*')
async def send_help(message: types.Message, state: FSMContext) -> None:
    await remove_last_inline(message, state)
    types.ReplyKeyboardRemove()
    await message.answer(phrasebook.HELP)


@dp.message_handler(commands=['history'], state='*')
async def show_history(message: types.Message, state: FSMContext) -> None:
    await remove_last_inline(message, state)
    types.ReplyKeyboardRemove()
    user_id = message.from_user.id
    # here should be limit of message length, but not implemented
    await message.answer(database.get_history(user_id))


@dp.message_handler(commands=['stats'], state='*')
async def show_stats(message: types.Message, state: FSMContext) -> None:
    await remove_last_inline(message, state)
    types.ReplyKeyboardRemove()
    user_id = message.from_user.id
    # here should be limit of message length, but not implemented
    await message.answer(database.get_stats(user_id))


@dp.callback_query_handler(state=States.waiting_for_film)
async def film_choice_callback_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    code = callback_query.data.split()[-1]
    user_id = callback_query.from_user.id

    if code == 'cancel':
        await state.finish()
        await bot.send_message(user_id, phrasebook.CANCEL)
    else:
        try:
            film_id = int(code)
        except ValueError:
            assert False, "invalid film id"

        data = await state.get_data()
        film_json = data['films'][film_id]

        await bot.send_photo(user_id, film_json['posterUrl'])
        await bot.send_message(user_id, phrasebook.construct_description(film_json))
        kb = keyboards.source_choice(film_json['name'])
        database.add_movie(user_id, film_json['name'])
        await bot.send_message(user_id, phrasebook.SOURCES, reply_markup=kb)
        await state.set_state(States.main.state)
        await state.update_data(Not_delete=True)

    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    await callback_query.answer()


@dp.message_handler(state='*')
@dp.message_handler(state='*')
async def find_films_by_name(message: types.Message, state: FSMContext) -> None:
    await remove_last_inline(message, state)
    film: str = message.text
    response_json: tp.Dict[str, tp.Any] = await kinopoisk.film2info(film)

    if 'films' not in response_json or not isinstance(response_json['films'], list) \
            or not len(response_json['films']) > 0:
        await message.answer(phrasebook.NOT_FOUND)
        return

    kb, films = keyboards.film_choice(response_json)
    await state.set_state(States.waiting_for_film.state)
    await state.update_data(films=films)
    await message.answer(phrasebook.FOUND, reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp)
