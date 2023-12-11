import asyncio
from config import dp, bot
from hands import main_h as main_h, callback as cb, allalg as alg, shoudle as sh
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# from hands.shoudle import scheduler


dp.include_router(main_h.router)
dp.include_router(cb.router)
dp.include_router(alg.router)


# dp.include_router(sh.router)

# @dp.message(F.text)
# async def s(message: Message):
#     await message.answer(str(message.from_user.id))

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# async def on_startup(dp):
#     asyncio.create_task(scheduler())


if __name__ == "__main__":
    asyncio.run(main())
