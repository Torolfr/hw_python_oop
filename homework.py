import datetime as dt
from typing import Union, List, Dict, Tuple


class Record:
    '''Класс для хранения данных в калькуляторе.'''
    def __init__(self,
                 amount: Union[int, float],
                 comment: str,
                 date: str = '') -> None:
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date == "":
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    '''Родительский класс Калькулятор.'''
    def __init__(self, limit: Union[int, float]) -> None:
        self.limit = limit
        self.records: List = []

    def add_record(self, record: Record) -> None:
        '''Метод для сохранения новой записи в объекте.'''
        self.records.append(record)

    def get_today_stats(self) -> Union[int, float]:
        '''Метод для подсчета дневного лимита.'''
        today_stats: float = 0
        for record in self.records:
            if record.date.day == dt.datetime.today().day:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self) -> Union[int, float]:
        '''Метод для получения статистики по объекту за последние 7 дней.'''
        week_stats: float = 0
        current_week = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if dt.date.today() >= record.date > current_week:
                week_stats += record.amount
        return week_stats

    def show_info(self) -> None:
        '''Метод для вывода записи'''
        for record in self.records:
            print(f'{record.amount} - {record.comment}: {record.date}')


class CaloriesCalculator(Calculator):
    '''Дочерний класс калькулятор калорий.'''
    def get_calories_remained(self) -> str:
        '''Метод для определения, сколько ещё калорий можно получить сегодня'''
        today_stats: float = self.get_today_stats()
        if today_stats < self.limit:
            calories: float = self.limit - today_stats
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {calories} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    '''Дочерний класс калькулятор денег.'''
    USD_RATE: float = 75.37
    EURO_RATE: float = 89.72
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        '''
        Метод для определения сколько ещё денег
        можно потратить сегодня в рублях, долларах или евро
        '''
        cur_dict: Dict[str, Tuple[float, str]]
        cur_dict = {'usd': (self.USD_RATE, 'USD'),
                    'eur': (self.EURO_RATE, 'Euro'),
                    'rub': (self.RUB_RATE, 'руб')}
        try:
            today_stats: float = self.get_today_stats()
            diff: float = self.limit - today_stats
            balance: float = round(diff / cur_dict[currency][0], 2)

            if balance > 0:
                return f'На сегодня осталось {balance} {cur_dict[currency][1]}'
            elif balance == 0:
                return 'Денег нет, держись'
            else:
                return ('Денег нет, держись: '
                        f'твой долг - {abs(balance)} {cur_dict[currency][1]}')
        except KeyError:
            return 'Вы указали недопустимую денежную едницу.'


cash_calculator = CashCalculator(1000)

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=1145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))
# должно напечататься
# На сегодня осталось 555 руб
