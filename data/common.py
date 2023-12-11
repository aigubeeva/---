import calendar
import locale

from aiogram.types import User
from datetime import datetime

from .schemas import CalendarLabels


async def get_user_locale(from_user: User) -> str:
    loc = from_user.language_code
    return locale.locale_alias[loc].split(".")[0]


class GenericCalendar:

    def __init__(
            self,
            locale: str = None,
            cancel_btn: str = None,
            today_btn: str = None,
            show_alerts: bool = False
    ) -> None:
        self._labels = CalendarLabels()
        if locale:
            with calendar.different_locale(locale):
                self._labels.days_of_week = list(calendar.day_abbr)
                self._labels.months = calendar.month_abbr[1:]

        if cancel_btn:
            self._labels.cancel_caption = cancel_btn
        if today_btn:
            self._labels.today_caption = today_btn

        self.min_date = None
        self.max_date = None
        self.show_alerts = show_alerts

    def set_dates_range(self, min_date: datetime, max_date: datetime):
        self.min_date = min_date
        self.max_date = max_date

    async def process_day_select(self, data, query):
        date = datetime(int(data.year), int(data.month), int(data.day))
        if self.min_date and self.min_date > date:
            await query.answer(
                f'Дата должна быть до {self.min_date.strftime("%d/%m/%Y")}',
                show_alert=self.show_alerts
            )
            return False, None
        elif self.max_date and self.max_date < date:
            await query.answer(
                f'Дата должна быть до {self.max_date.strftime("%d/%m/%Y")}',
                show_alert=self.show_alerts
            )
            return False, None
        await query.message.delete_reply_markup()
        return True, date
