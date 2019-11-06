from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union


@dataclass
class Note:
    note: str


@dataclass
class Developer:
    name: str
    dilution: str
    iso: int
    temp: str
    thirtyfive: Optional[Union[int, float, str]] = None
    hundrettwenty: Optional[Union[int, float, str]] = None
    sheet: Optional[Union[int, float, str]] = None
    notes: Optional[List[Note]] = None


@dataclass
class Film:
    name: str
    developers: List[Developer]


@dataclass
class Films:
    updated: datetime
    films: List[Film]
