import re

from DataLoader import DataLoader
from TicketParser import TicketParser


class TicketSearch:
    def __init__(self):
        self.data_loader = DataLoader()
        self.ticket_parser = TicketParser()

    def search(self):
        """Поиск билетов"""

        api_key = input('Введите api ключ разработчика: ')
        from_code = input('IATA код аэропорта из которого хотите отправиться: ')
        to_code = input('IATA код аэропорта в который хотите прибыть: ')
        date = input('Введите дату вылета в формате YYYY-MM-DD: ')

        if re.fullmatch('\d\d\d\d-\d\d-\d\d', date) is None:
            print('Дата не соответствует формату YYYY-MM-DD')
            return

        flights = self.data_loader.load(api_key, from_code, to_code, date)

        if flights is None:
            return

        for ticket in self.ticket_parser.get_tickets(flights, from_code, to_code):
            print(ticket)

        print("Данные получены с помощью сервиса Яндекс.Расписание http://rasp.yandex.ru")


if __name__ == '__main__':
    ticket_search = TicketSearch()
    ticket_search.search()

