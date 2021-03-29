import datetime as dt
from typing import Dict, List, Optional, Tuple


class Record:
    """Класс для хранения данных в калькуляторе."""
    date_format = '%d.%m.%Y'

    def __init__(self,
                 amount: int,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    """Родительский класс Калькулятор."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """Метод для сохранения новой записи в объекте."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Метод для подсчета дневного лимита."""
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)

    def get_week_stats(self) -> float:
        """Метод для получения статистики по объекту за последние 7 дней."""
        week_stats: float = 0
        last_week = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if last_week < record.date <= dt.date.today():
                week_stats += record.amount
        return week_stats

    def get_balance(self) -> float:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Дочерний класс калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """
        Метод для определения, сколько ещё калорий можно получить сегодня.
        """
        today_stats: float = self.get_today_stats()
        if today_stats < self.limit:
            calories: float = self.get_balance()
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {calories} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Дочерний класс калькулятор денег."""
    USD_RATE: float = 75.37
    EURO_RATE: float = 89.72
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод для определения сколько ещё денег
        можно потратить сегодня в рублях, долларах или евро.
        """
        cur_dict: Dict[str, Tuple[float, str]]
        cur_dict = {'usd': (self.USD_RATE, 'USD'),
                    'eur': (self.EURO_RATE, 'Euro'),
                    'rub': (self.RUB_RATE, 'руб')}
        if currency not in cur_dict:
            raise ValueError('Вы указали недопустимую денежную едницу.')
        currency_rate, currency_unit = cur_dict[currency]
        balance: float = round(self.get_balance() / currency_rate, 2)
        if balance == 0:
            return 'Денег нет, держись'
        if balance > 0:
            return f'На сегодня осталось {balance} {currency_unit}'
        balance = abs(balance)
        return ('Денег нет, держись: '
                f'твой долг - {balance} {currency_unit}')
