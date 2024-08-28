import datetime
import pytz


class Service():


    async def create_moscow_time(self):
            return datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%H:%M %d/%m")

    async def create_day_year(self):
        return datetime.date.today().strftime("%d.%m.%Y")






