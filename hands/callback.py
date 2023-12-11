from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from data.kb import nastr_nap, timeset, main

from config import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from aiogram.filters.callback_data import CallbackData

router: Router = Router()


@router.callback_query(F.data == 'stsled')
async def fik(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer("Хорошо! введи /reg для заполнения данных")


@router.message(F.text == "Настройка напоминаний")
async def nap(message: Message):
    await message.answer("Хорошо! Вот настройки", reply_markup=nastr_nap)


@router.message(F.text == "Присылать напоминания")
async def napda(message: Message):
    await message.answer("Как часто напоминать?\nКаждые..", reply_markup=timeset)


@router.message(F.text == 'Календарь месячных')
async def nav_cal_handler(message: Message):
    await message.answer(
        "Выберите:",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(locale=await get_user_locale(callback_query.from_user), show_alerts=True)
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))

    selected, date = await calendar.process_selection(callback_query, callback_data)

    if selected:
        await callback_query.message.answer(f'\n\nВы выбрали: {date.strftime("%d/%m/%Y")}')
        day = date.strftime("%d")
        if 1 <= int(day) <= 7:
            await callback_query.message.answer(f'1-7 - месячные')
        if 8 <= int(day) <= 9:
            await callback_query.message.answer(f'8-9 - возможно зачатие')
        if 10 <= int(day) <= 14:
            await callback_query.message.answer(f'10-14 - овуляция')
        if 15 <= int(day) <= 16:
            await callback_query.message.answer(f'15-16 - возможно зачатие')
        if 17 <= int(day) <= 28:
            await callback_query.message.answer(f'17-28 - низкая вероятность зачатия')


async def send_message_interval(chat_id):
    await bot.send_message(chat_id=chat_id, text='Пора выпить водички!')


scheduler1 = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler2 = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler3 = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler4 = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler5 = AsyncIOScheduler(timezone="Europe/Moscow")


@router.message(F.text == "Не присылать напоминания")
async def napne(message: Message):
    try:
        scheduler1.remove_job(job_id='1')
    except:
        try:
            scheduler2.remove_job(job_id='2')
        except:
            try:
                scheduler3.remove_job(job_id='3')
            except:
                try:
                    scheduler4.remove_job(job_id='4')
                except:
                    try:
                        scheduler5.remove_job(job_id='5')
                    except:
                        pass
    await message.answer("Настройки обновлены ", reply_markup=nastr_nap)


@router.message(F.text.in_(["10 мин", "20 мин", "30 мин", "1 час", "2 часа"]))
async def nap1(message: Message):
    if message.text == '10 мин':
        try:
            scheduler2.remove_job(job_id='2')
        except:
            try:
                scheduler3.remove_job(job_id='3')
            except:
                try:
                    scheduler4.remove_job(job_id='4')
                except:
                    try:
                        scheduler5.remove_job(job_id='5')
                    except:
                        pass
            try:
                scheduler1.add_job(func=send_message_interval, trigger='interval', \
                                   seconds=600, id='1', kwargs={'chat_id': message.chat.id})
                scheduler1.start()
                await message.answer("Настройки обновлены ", reply_markup=nastr_nap)
            except:
                await message.answer("Настройки обновлены или вы нажали повторно")


    elif message.text == '20 мин':
        try:
            scheduler1.remove_job(job_id='1')
        except:
            try:
                scheduler3.remove_job(job_id='3')
            except:
                try:
                    scheduler4.remove_job(job_id='4')
                except:
                    try:
                        scheduler5.remove_job(job_id='5')
                    except:
                        pass
        try:
            scheduler2.add_job(func=send_message_interval, trigger='interval', \
                               seconds=1200, id='2', kwargs={'chat_id': message.chat.id})
            scheduler2.start()
            await message.answer("Настройки обновлены ", reply_markup=nastr_nap)
        except:
            await message.answer("Настройки обновлены или вы нажали повторно")

    elif message.text == '30 мин':
        try:
            scheduler1.remove_job(job_id='1')
        except:
            try:
                scheduler2.remove_job(job_id='2')
            except:
                try:
                    scheduler4.remove_job(job_id='4')
                except:
                    try:
                        scheduler5.remove_job(job_id='5')
                    except:
                        pass
        try:
            scheduler3.add_job(func=send_message_interval, trigger='interval', \
                               seconds=1800, id='3', kwargs={'chat_id': message.chat.id})
            scheduler3.start()
            await message.answer("Настройки обновлены ", reply_markup=nastr_nap)
        except:
            await message.answer("Настройки обновлены или вы нажали повторно")

    elif message.text == '1 час':
        try:
            scheduler1.remove_job(job_id='1')
        except:
            try:
                scheduler2.remove_job(job_id='2')
            except:
                try:
                    scheduler3.remove_job(job_id='3')
                except:
                    try:
                        scheduler5.remove_job(job_id='5')
                    except:
                        pass
        try:
            scheduler4.add_job(func=send_message_interval, trigger='interval', \
                               seconds=3600, id='4', kwargs={'chat_id': message.chat.id})
            scheduler4.start()
            await message.answer("Настройки обновлены ", reply_markup=nastr_nap)
        except:
            await message.answer("Настройки обновлены или вы нажали повторно")

    elif message.text == '2 часа':
        try:
            scheduler1.remove_job(job_id='1')
        except:
            try:
                scheduler2.remove_job(job_id='2')
            except:
                try:
                    scheduler3.remove_job(job_id='3')
                except:
                    try:
                        scheduler4.remove_job(job_id='4')
                    except:
                        pass
        try:
            scheduler5.add_job(func=send_message_interval, trigger='interval', \
                               seconds=7200, id='5', kwargs={'chat_id': message.chat.id})
            scheduler5.start()
            await message.answer("Настройки обновлены ", reply_markup=nastr_nap)
        except:
            await message.answer("Настройки обновлены или вы нажали повторно")


@router.message(F.text == 'Назад в главное меню')
async def back(message: Message):
    await message.answer('Назад', reply_markup=main)
