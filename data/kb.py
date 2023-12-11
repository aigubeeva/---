from aiogram.types import InlineKeyboardButton, KeyboardButton
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


start_zdorov = create_inline_key(1, **{'stsled': 'Начать следить за здоровьем!'})
cncl = create_inline_key(1, **{'cancel': 'Отмена'})
main = create_reply_key(2, 'Календарь месячных', 'Настройка напоминаний')
nastr_nap = create_reply_key(2, 'Присылать напоминания', 'Не присылать напоминания', 'Назад в главное меню')
timeset = create_reply_key(2, '10 мин', '20 мин', '30 мин', '1 час', '2 часа', 'Назад в главное меню')
