from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging
from Mydata.db.db_helper import add_items_db, get_data_from_users, update_items_db
from Mydata.kb import main, cncl

router: Router = Router()


def chk_num(d):
    c = []
    for i in d:
        if i in '1234567890':
            c.append(True)
        else:
            c.append(False)
    return all(c)


class Person(StatesGroup):
    height = State()
    weight = State()
    age = State()
    sex = State()
    y = State()


@router.message(Command("reg"))
async def st(message: Message, state: FSMContext):
    usr_id = await get_data_from_users(message.from_user.id)
    if usr_id and message.text:
        await message.answer("Заново зарегестрируем")
        await message.answer('Какой у тебя рост?', reply_markup=cncl)
        await state.set_state(Person.height)
    else:
        await message.answer("Какой у тебя рост?", reply_markup=cncl)
        await state.set_state(Person.height)


@router.callback_query(F.data == "cancel")
async def cancel_handler(cb: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await cb.answer("Вы отменили действие")


@router.message(Person.height)
async def st(message: Message, state: FSMContext):
    await state.update_data(height=message.text.lower())
    user_data = await state.get_data()
    d = [i for i in user_data["height"]]
    if chk_num(d):
        await message.answer("Сколько ты весишь?", reply_markup=cncl)
        await state.set_state(Person.weight)
    else:
        await message.answer("Введи число!")


@router.message(Person.weight)
async def st2(message: Message, state: FSMContext):
    await state.update_data(weight=message.text.lower())
    user_data = await state.get_data()
    d = [i for i in user_data["weight"]]
    if chk_num(d):
        await message.answer("Сколько тебе лет?", reply_markup=cncl)
        await state.set_state(Person.age)
    else:
        await message.answer('Введи число!')


@router.message(Person.age)
async def st3(message: Message, state: FSMContext):
    await state.update_data(age=message.text.lower())
    user_data = await state.get_data()
    d = [i for i in user_data["age"]]
    if chk_num(d):
        await message.answer("Твой пол? [М/Ж]", reply_markup=cncl)
        await state.set_state(Person.sex)
    else:
        await message.answer('Введи число!')


@router.message(Person.sex)
async def st4(message: Message, state: FSMContext):
    await state.update_data(sex=message.text.lower())
    user_data = await state.get_data()
    if user_data["sex"] == "м" or user_data["sex"] == "ж":
        uh, uw, ua, us = [i[1] for i in user_data.items()]
        await message.answer(f"Рост: {uh},\nВес: {uw},\nВозраст: {ua},\nПол: {us}\n\nВерно? [Да/Нет]\n")
        await state.set_state(Person.y)
    else:
        await message.answer('Введите М (мужской) или Ж (женский)')


@router.message(Person.y)
async def st5(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(y=message.text.lower())
    user_data = await state.get_data()

    if user_data["y"] == "да" or user_data["y"] == "д":
        uh, uw, ua, us = [i[1] for i in user_data.items()][0:-1]
        usr_id = await get_data_from_users(message.from_user.id)
        logging.info(usr_id)
        if not usr_id == None:
            if usr_id[0] == message.from_user.id:
                await update_items_db(user_id=usr_id[0], uh=uh, uw=uw, ua=ua, us=us)
            else:
                await add_items_db(args=[str(message.from_user.id), uh, uw, ua, '0', us], db=1)
        else:
            await add_items_db(args=[str(message.from_user.id), uh, uw, ua, '0', us], db=1)

        await message.answer("Готово!\nЧтобы зарегестрироваться заново - /reg")

        if us.lower() == 'м':
            await message.answer(f'Твоя норма воды: {int(uw) * 35} мл', reply_markup=main)
            await state.clear()
        else:
            await message.answer(f'Твоя норма воды: {int(uw) * 31} мл', reply_markup=main)
            await state.clear()
    elif user_data["y"] == "нет" or user_data["y"] == "н":
        await message.answer('Хорошо, форма отменена')
        await state.clear()
    else:
        await message.answer('/cancel для отмены, введите Да или Нет')
