from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
from Mydata.db.make_table import make_table

router: Router = Router()


@router.message(Command('figure'))
async def send_figure(message: Message):
    await make_table(message.from_user.id)
    figure = FSInputFile("Mydata\Figure_1.png", "Figure_1.png")
    await message.answer_photo(photo=figure, caption="Ваша статистика")
