import sqlite3
from typing import Any

from data import config

DATABASE = config.DB


def read_data(query) -> list:
    """
    Function. Read data from db (tuple list formatted).
    :param query: query string
    :return: list
    """
    with sqlite3.connect(f"./data/{DATABASE}") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result: list[tuple] = cursor.fetchall()
        connection.commit()
    return result


def write_data(query) -> None:
    """
    Function. Write data to db.
    :param query: query string.
    :return: None
    """
    with sqlite3.connect(f"./data/{DATABASE}") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()


def read_data_row(query) -> list[dict[str, Any]]:
    with sqlite3.connect(f"./data/{DATABASE}") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        result: list = cursor.fetchall()
        connection.commit()
    return [dict(row) for row in result]
