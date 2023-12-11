from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from data import kb
from aiogram.filters import CommandStart, Command
from config import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import logging
from hands.allalg import chk_num
from data.db.db_helper import get_data_from_users

router: Router = Router()


class Chek_vada(StatesGroup):
    pil = State()


async def send_message_cron(chat_id, state):
    await bot.send_message(chat_id=chat_id, text='Сколько мл воды ты выпил(а) сегодня?')
    await state.set_state(Chek_vada.pil)


@router.message(Chek_vada.pil)
async def send_message(message: Message, state: FSMContext):
    usr_data = await get_data_from_users(message.from_user.id)
    if usr_data == None:
        await message.answer("Зарегистрируйтесь - /reg")
    else:
        if chk_num(message.text):
            await state.update_data(pil=message.text)
            usr_data = await get_data_from_users(message.from_user.id)

            logging.info(usr_data[2])
            logging.info(usr_data[-1])

            if usr_data[2] * 35 > int(message.text) and usr_data[-1] == "м":
                await message.answer(
                    f'Вы выпили недостаточное количество воды!\nВам еще нужно выпить {usr_data[2] * 35 - int(message.text)} мл')
                await state.clear()
            elif usr_data[2] * 31 > int(message.text):
                await message.answer(
                    f'Вы выпили недостаточное количество воды!\nВам еще нужно выпить {usr_data[2] * 31 - int(message.text)} мл')
                await state.clear()
        else:
            await message.answer('Введи число в мл!')


@router.message(CommandStart())
async def st(message: Message, state: FSMContext):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    logging.info(str(datetime.now()))

    scheduler.add_job(send_message_cron, trigger="cron", hour='22',
                      minute='11', start_date=datetime.now(),
                      kwargs={
                          'chat_id': message.chat.id,
                          "state": state
                      })

    scheduler.start()

    await message.answer(f'Привет! {message.from_user.first_name}! Я твой личный помощник по здоровью.')
    await message.answer('Я помогать:\n1) следить за твоим водным балансом \n2) вести календарь месячных',
                         reply_markup=kb.start_zdorov)

# print('2023-12-11 19:30:02.753967'[11:13]) # hour
# print('2023-12-11 19:30:02.753967'[14:16]) # min
# print('2023-12-11 19:30:02.753967'[17:19]) # sec
