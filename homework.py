import datetime as dt

# from typing import Union, List, Optional, Dict, Tuple


class Record:
    '''Класс для хранения данных в калькуляторе.'''
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date == "":
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    '''Родительский класс Калькулятор.'''
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        '''Метод для сохранения новой записи в объекте.'''
        self.records.append(record)

    def get_today_stats(self):
        '''Метод для подсчета дневного лимита.'''
        today_stats = 0
        for record in self.records:
            if record.date.day == dt.datetime.today().day:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        '''Метод для получения статистики по объекту за последние 7 дней.'''
        week_stats = 0
        current_week = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if dt.date.today() >= record.date > current_week:
                week_stats += record.amount
        return week_stats

    def show_info(self):
        '''Метод для вывода записи'''
        for record in self.records:
            print(f'{record.amount} - {record.comment}: {record.date}')


class CaloriesCalculator(Calculator):
    '''Дочерний класс калькулятор калорий.'''
    def get_today_stats(self):
        today_stats = super().get_today_stats()
        return f'{today_stats} калорий уже съедено сегодня'

    def get_calories_remained(self):
        today_stats = super().get_today_stats()
        if today_stats < self.limit:
            result = self.limit - today_stats
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {result} кКал'
        else:
            return 'Хватит есть!'

    def get_week_stats(self):
        week_stats = super().get_week_stats()
        return f'{week_stats} Ккал получено за последние 7 дней'


class CashCalculator(Calculator):
    '''Дочерний класс калькулятор денег.'''
    USD_RATE: float = 75.37
    EURO_RATE: float = 89.72

    def get_today_stats(self):
        today_stats = super().get_today_stats()
        return f'{today_stats} руб. уже потрачено сегодня'

    def get_today_cash_remained(self, currency):
        today_stats = super().get_today_stats()
        balance = round(self.limit - today_stats, 2)
        USD_RATE = 75.37
        EURO_RATE = 89.72

        def compare(balance, limit, currency):
            '''
            Вспомогательная функция для сравнения остатка суммы
            и дневного лимита без учета денежной единицы
            '''
            if balance > 0:
                return f'На сегодня осталось {balance} {currency}'
            elif balance == 0:
                return 'Денег нет, держись'
            elif balance < 0:
                return f'Денег нет, держись: твой долг -  {abs(balance)} {currency}'

        if currency == 'rub':
            return compare(balance, self.limit, 'руб')
        elif currency == 'usd':
            usd_balance = round(balance / USD_RATE, 2)
            usd_limit = self.limit / USD_RATE
            return compare(usd_balance, usd_limit, 'USD')
        elif currency == 'eur':
            eur_balance = round(balance / EURO_RATE, 2)
            eur_limit = self.limit / EURO_RATE
            return compare(eur_balance, eur_limit, 'Euro')
        else:
            return 'Вы указали недопустимую денежную едницу.'

    def get_week_stats(self):
        week_stats = super().get_week_stats()
        return f'{week_stats} руб. потрачено за последние 7 дней'


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

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб
