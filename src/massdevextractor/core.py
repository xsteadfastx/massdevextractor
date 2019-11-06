"""Core module."""
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin

import orjson
import pandas as pd
from gazpacho import Soup, get
from structlog import get_logger

from massdevextractor import objects

LOGGER = get_logger()

BASE_URL = "https://www.digitaltruth.com/chart/"


def get_film_overview() -> List[Soup]:
    url = urljoin(BASE_URL, "print.php")
    LOGGER.debug("created_url", url=url)
    html = get(url)
    soup = Soup(html)
    films = [film for film in soup.find("a") if "Film" in film.attrs["href"]]
    LOGGER.debug("got_films", films=films)

    return films


def create_film_urls(films: List[Soup]) -> List[str]:
    urls = [urljoin(BASE_URL, film.attrs["href"]) for film in films]
    LOGGER.debug("got_film_urls", urls=urls)

    return urls


def get_film_data(films_urls: List[str]) -> List[pd.core.frame.DataFrame]:
    film_data: List[pd.core.frame.DataFrame] = []
    for film in films_urls:
        url = film.replace(" ", "%20")
        LOGGER.info("getting_film", url=url)
        try:
            tables = pd.read_html(url)
            LOGGER.debug("got_film_data", data=tables)
        except ValueError:
            LOGGER.exception("no_table_found")
        table = tables[0]
        table.columns = [
            "film",
            "developer",
            "dilution",
            "iso",
            "thirtyfive",
            "hundrettwenty",
            "sheet",
            "temp",
            "notes",
        ]
        table = table.replace({pd.np.nan: None})
        LOGGER.debug("add_film_data", data=table)
        film_data.append(table)
    return film_data


def find_notes(
    note_string: Optional[str], notes: Dict[str, str]
) -> Optional[List[objects.Note]]:
    if not note_string:
        return None
    matcher = re.compile(r"\[([a-zA-z0-9]+?)\]")
    note_list: Optional[List[objects.Note]] = []
    for match in matcher.findall(note_string):
        if match in notes.keys():
            LOGGER.info("found_note", note=match)
            note_list.append(objects.Note(note=notes[match]))
    if note_list:
        return note_list
    else:
        return None


def create_objects(
    film_data: List[pd.core.frame.DataFrame], notes: Dict[str, str]
) -> objects.Films:
    films: List[objects.Film] = []
    for data in film_data:
        developers: List[objects.Developer] = []
        for _, developer in data.iterrows():
            LOGGER.info(
                "creating_developer_obj",
                film=developer.film,
                developer=developer.developer,
            )
            developers.append(
                objects.Developer(
                    name=developer.developer,
                    dilution=developer.dilution,
                    iso=developer.iso,
                    temp=developer.temp,
                    thirtyfive=developer.thirtyfive,
                    hundrettwenty=developer.hundrettwenty,
                    sheet=developer.sheet,
                    notes=find_notes(developer.notes, notes),
                )
            )
        films.append(objects.Film(name=data.iloc[0].film, developers=developers))

    return objects.Films(films=films, updated=datetime.utcnow())


def write_json(films_object: objects.Films) -> None:
    data: bytes = orjson.dumps(films_object, option=orjson.OPT_SERIALIZE_DATACLASS)
    with open("foo.json", "w") as f:
        json.dump(json.loads(data), f, indent=4)


def get_notes() -> Dict[str, str]:
    url = urljoin(BASE_URL, "notes.php")
    tables = pd.read_html(url)
    table = tables[0]

    return table.set_index(0).T.to_dict("records")[0]


def main() -> None:
    LOGGER.info("getting_notes")
    notes = get_notes()
    LOGGER.debug("notes", data=notes)
    LOGGER.info("getting_films")
    films = get_film_overview()
    LOGGER.info("getting_film_urls")
    film_urls = create_film_urls(films)
    LOGGER.info("getting_film_data")
    film_data = get_film_data(film_urls)
    LOGGER.debug("film_data", data=film_data)
    LOGGER.info("creating_films_object")
    films_object = create_objects(film_data, notes)
    LOGGER.info("write_json")
    write_json(films_object)
