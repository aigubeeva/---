from datetime import datetime, timedelta


def lastMenstruation_ovulation_fertility_nextMenstruation(date, cycle):
    last_menstruation = datetime.strptime(date, "%d/%m/%Y")
    last_menstruation_formatted = last_menstruation.strftime("%#d.%m.%#Y")
    last_menstruation_tx = f"Твои последние месячные: {last_menstruation_formatted}"

    # Find ovulation day
    ovulation_date = last_menstruation + timedelta(days=cycle - 14)
    ovulation_date_formatted = ovulation_date.strftime("%#d.%m.%#Y")

    # Find your fertility days
    fertility_start = ovulation_date + timedelta(days=-3)
    fertility_start_formatted = fertility_start.strftime("%#d.%m.%#Y")
    fertility_end = ovulation_date + timedelta(days=1)
    fertility_end_formatted = fertility_end.strftime("%#d.%m.%#Y")

    # Find next menstruation
    next_menstruation = last_menstruation + timedelta(days=cycle)
    next_menstruation_formatted = next_menstruation.strftime("%#d.%m.%#Y")

    return last_menstruation_tx, next_menstruation_formatted, ovulation_date_formatted


async def ask_cycle(date, cycle_tx):
    return lastMenstruation_ovulation_fertility_nextMenstruation(date, cycle_tx)

# print(ask_cycle(date='01/12/2023', cycle_tx=28))
