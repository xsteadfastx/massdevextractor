# pylint: disable=missing-module-docstring,missing-class-docstring
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Note:
    note: str


# pylint: disable=too-many-instance-attributes
@dataclass
class Developer:
    name: str
    dilution: Optional[str]
    iso: Optional[str]
    temp: Optional[str]
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
