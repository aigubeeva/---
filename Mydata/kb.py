from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_inline_key(width: int, *args: str, **kwargs: str):
    kb_bld: InlineKeyboardBuilder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(text=kb_bld[button] if button in kb_bld else button, callback_data=button))
    if kwargs:
        for key, button in kwargs.items():
            buttons.append(InlineKeyboardButton(text=button, callback_data=key, ))
    kb_bld.row(*buttons, width=width)
    return kb_bld.as_markup()


def create_reply_key(width: int, *args: str, **kwargs: str):
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))
    if kwargs:
        for key, val in kwargs.items():
            buttons.append(KeyboardButton(text=val))
    menu.row(*buttons, width=width)

    return menu.as_markup(resize_keyboard=True)


del_kb = ReplyKeyboardRemove()

start_zdorov = create_inline_key(1, **{'stsled': 'Начать следить за здоровьем!'})
cncl = create_inline_key(1, **{'cancel': 'Отмена'})
main = create_reply_key(2, 'Календарь месячных', 'Настройка напоминаний', 'Месячные')
nastr_nap = create_reply_key(2, 'Присылать напоминания', 'Не присылать напоминания', 'Назад в главное меню')
timeset = create_reply_key(2, '10 мин', '20 мин', '30 мин', '1 час', '2 часа', 'Назад в главное меню')
ocen1 = create_reply_key(4, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
ocen2 = create_reply_key(2, 'злость', 'радость', 'тревога', 'страх', 'отвращение', 'грусть', 'скука', 'интерес',
                         'любовь')

period_s = create_reply_key(2, 'Сегодня месячные', 'Назад в главное меню')
