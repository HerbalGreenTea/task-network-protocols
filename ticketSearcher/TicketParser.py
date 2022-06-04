import re

from PlaneData import DataAirport
from PlaneData import DataFlight


class TicketParser:
    def __init__(self):
        self.datetime_regex = re.compile(r'([\d]{4})-([\d]{2})-([\d]{2})T(\d\d:\d\d):\d\d([\+\-]\d\d):\d\d')
        self.ticket_form = (
                ".................................................................\n" +
                "{flight_number}, {company}\n" +
                "{from_city} -> {to_city}\n" +
                "{from_airport} -> {to_airport}\n" +
                "{from_airport_code} -> {to_airport_code}\n" +
                "{from_datetime} -> {to_datetime}\n" +
                "{plane_type}\n" +
                "В полете: {hours} ч {minutes} мин\n" +
                ".................................................................\n"
        )

    def __parse_ticket__(self, flight):
        """Форматривание для вывода информации и о рейсе"""

        duration = flight.duration // 60
        hours = 0
        while duration >= 60:
            duration -= 60
            hours += 1

        return self.ticket_form.format(
            flight_number=flight.number,
            company=flight.company,
            from_city=flight.start.city,
            to_city=flight.end.city,
            from_airport=flight.start.name,
            to_airport=flight.end.name,
            from_airport_code=flight.start.code,
            to_airport_code=flight.end.code,
            from_datetime=flight.depart_datetime,
            to_datetime=flight.arrival_datetime,
            plane_type=flight.plane_type,
            hours=hours,
            minutes=duration
        )

    def __parse_datetime__(self, date):
        """Парсинг даты и времени"""

        data = [x for x in self.datetime_regex.findall(date)[0]]

        datetime = '{day}.{month}.{year} - {time}'.format(
            day=data[2],
            month=data[1],
            year=data[0],
            time=data[3]
        )

        return datetime

    def get_tickets(self, flights, start_code, end_code) -> str:
        """Парсинг билетов"""

        if len(flights) == 0:
            return 'Билеты не найдены'

        for flight in flights:
            flight_number = flight['thread']['number']
            start_city, end_city = flight['thread']['title'].split(' — ')
            start_point = DataAirport(flight['from']['title'], start_code, start_city)
            end_point = DataAirport(flight['to']['title'], end_code, end_city)
            company = flight['thread']['carrier']['title']
            depart_datetime = self.__parse_datetime__(flight['departure'])
            arrival_datetime = self.__parse_datetime__(flight['arrival'])
            duration = flight['duration']
            plane_type = flight['thread']['vehicle']

            flight = DataFlight(
                flight_number,
                start_point,
                end_point,
                company,
                depart_datetime,
                arrival_datetime,
                duration,
                plane_type
            )

            yield self.__parse_ticket__(flight)

