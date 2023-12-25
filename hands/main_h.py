from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from config import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import logging
from hands.allalg import chk_num
from hands.dict import rand_com
from Mydata.db.db_helper import get_data_from_users, add_items_db, update_shnap
from Mydata.db.make_table import make_table
from Mydata.kb import ocen1, ocen2, start_zdorov, main
from .callback import stop_shedulers, start_shedulers
from .allalg import chk_num

router: Router = Router()


class EmotionalState(StatesGroup):
    basic = State()


async def send_message_cron2(chat_id, state, text):
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_message(chat_id=chat_id, text='Оцени от 0 до 10', reply_markup=ocen1)
    await state.set_state(EmotionalState.basic)


@router.message(EmotionalState.basic)
async def basic(message: Message, state: FSMContext):
    await add_items_db(args=[str(message.from_user.id), message.text], db=2)
    await make_table(user_id=message.from_user.id)
    usr_data = await get_data_from_users(message.from_user.id)
    if usr_data == None:
        await message.answer("Зарегестрируйтесь - /reg")
        await state.clear()
    else:
        await message.answer('Какие эмоции сегодня преобладали?', reply_markup=ocen2)
        await state.clear()


@router.message(
    F.text.in_(['злость', 'радость', 'тревога', 'страх', 'отвращение', 'грусть', 'скука', 'интерес', 'любовь']))
async def next_step(message: Message):
    match message.text:
        case 'злость':
            await message.answer(await rand_com(1), reply_markup=main)
        case 'радость':
            await message.answer(await rand_com(2), reply_markup=main)
        case 'тревога':
            await message.answer(await rand_com(3), reply_markup=main)
        case 'страх':
            await message.answer(await rand_com(4), reply_markup=main)
        case 'отвращение':
            await message.answer(await rand_com(5), reply_markup=main)
        case 'грусть':
            await message.answer(await rand_com(6), reply_markup=main)
        case 'скука':
            await message.answer(await rand_com(7), reply_markup=main)
        case 'интерес':
            await message.answer(await rand_com(8), reply_markup=main)
        case 'любовь':
            await message.answer(await rand_com(9), reply_markup=main)


class CheckWater(StatesGroup):
    pil = State()


async def send_message_cron1(chat_id, state, text):
    await bot.send_message(chat_id=chat_id, text=text)
    await state.set_state(CheckWater.pil)


@router.message(CheckWater.pil)
async def pilvada(message: Message, state: FSMContext):
    usr_data = await get_data_from_users(message.from_user.id)
    if usr_data == None:
        await message.answer("Зарегестрируйтесь - /reg")
        await state.clear()
    else:
        if chk_num(message.text):
            await state.update_data(pil=message.text)
            usr_data = await get_data_from_users(message.from_user.id)

            # logging.info(usr_data[2])
            # logging.info(usr_data[-1])

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
    stopscheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    startscheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler11 = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler22 = AsyncIOScheduler(timezone="Europe/Moscow")
    logging.info(str(datetime.now()))
    stopscheduler.add_job(stop_shedulers, trigger="cron", hour='21',
                          minute='05', start_date=datetime.now(),
                          kwargs={
                              'user_id': message.from_user.id
                          })
    startscheduler.add_job(start_shedulers, trigger="cron", hour='07',
                           minute='00', start_date=datetime.now(),
                           kwargs={
                               'user_id': message.from_user.id
                           })
    scheduler11.add_job(send_message_cron1, trigger="cron", hour='21',
                        minute='00', start_date=datetime.now(),
                        kwargs={
                            'chat_id': message.chat.id,
                            "state": state,
                            'text': 'Сколько мл воды ты выпил(а) сегодня?'
                        })
    scheduler22.add_job(send_message_cron2, trigger="cron", hour='21',
                        minute='10', start_date=datetime.now(),
                        kwargs={
                            'chat_id': message.chat.id,
                            "state": state,
                            'text': 'Пришло время оценить твое эмоциональное состояние!'
                        })

    startscheduler.start()
    stopscheduler.start()
    scheduler11.start()
    scheduler22.start()

    await message.answer(f'Привет! {message.from_user.first_name}! Я твой личный помощник по здоровью.')
    await message.answer(
        'Я умею:\n1) отслеживать и напоминать о  количестве выпитой воды \n2) вести календарь месячных',
        reply_markup=start_zdorov)

# print('2023-12-11 19:30:02.753967'[11:13]) # hour
# print('2023-12-11 19:30:02.753967'[14:16]) # min
# print('2023-12-11 19:30:02.753967'[17:19]) # sec
