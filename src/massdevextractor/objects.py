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
    iso: str
    temp: str
    thirtyfive: Optional[str] = None
    hundrettwenty: Optional[str] = None
    sheet: Optional[str] = None
    notes: Optional[List[Note]] = None


@dataclass
class Film:
    name: str
    developers: List[Developer]


@dataclass
class Films:
    updated: datetime
    films: List[Film]
