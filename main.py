import asyncio
from config import dp, bot
from hands import dia, main_h as main_h, callback as cb, allalg as alg
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

dp.include_router(main_h.router)
dp.include_router(cb.router)
dp.include_router(alg.router)
dp.include_router(dia.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
