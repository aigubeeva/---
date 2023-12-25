from aiogram import Dispatcher, Bot
import logging
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] - %(asctime)s -  %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                    )

bot = Bot(token="6753951909:AAH2o4Ivtltfifdrwy-qtjO_SpHfkrCvh9s")
dp = Dispatcher(storage=MemoryStorage())
