import datetime as dt
from typing import Dict, List, Optional, Tuple

DATE_FORMAT = '%d.%m.%Y'


class Record:
    """Класс для хранения данных в калькуляторе."""

    def __init__(self,
                 amount: float,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


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
        today = dt.date.today()
        last_week = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if last_week < record.date <= today)

    def get_balance(self) -> float:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Дочерний класс калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """
        Метод для определения, сколько ещё калорий можно получить сегодня.
        """
        calories: float = self.get_balance()
        if calories > 0:
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
        money: Dict[str, Tuple[float, str]]
        money = {'usd': (self.USD_RATE, 'USD'),
                 'eur': (self.EURO_RATE, 'Euro'),
                 'rub': (self.RUB_RATE, 'руб')}
        balance = self.get_balance()
        if balance == 0:
            return 'Денег нет, держись'
        if currency not in money:
            return 'Вы указали недопустимую денежную единицу.'
        currency_rate: float
        currency_unit: str
        currency_rate, currency_unit = money[currency]
        balance_unit: float = round(balance / currency_rate, 2)
        if balance > 0:
            return f'На сегодня осталось {balance_unit} {currency_unit}'
        balance_unit = abs(balance_unit)
        return ('Денег нет, держись: '
                f'твой долг - {balance_unit} {currency_unit}')
