from dataclasses import dataclass
from typing import Any


@dataclass
class DataAirport:
    name: Any
    code: Any
    city: Any


@dataclass
class DataFlight:
    number: Any
    start: DataAirport
    end: DataAirport
    company: Any
    depart_datetime: str
    arrival_datetime: str
    duration: Any
    plane_type: Any
