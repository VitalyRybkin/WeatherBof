import logging
import sqlite3
from sqlite3 import DatabaseError
from typing import Any

from data import config

DATABASE = config.DB


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s | %(message)s")
file_handler = logging.FileHandler("./logs/db_conn_center.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def read_data(query) -> list:
    """
    Function. Read data from db (tuple list formatted).
    :param query: query string
    :return: list
    """
    try:
        with sqlite3.connect(f"./data/{DATABASE}") as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result: list[tuple] = cursor.fetchall()
            connection.commit()
    except DatabaseError as e:
        logging.error("Database read data error: ", e)

    return result


def write_data(query) -> None:
    """
    Function. Write data to db.
    :param query: query string.
    :return: None
    """
    try:
        with sqlite3.connect(f"./data/{DATABASE}") as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
    except DatabaseError as e:
        logging.error("Database write data error: ", e)


def read_data_row(query) -> list[dict[str, Any]]:
    """
    Function. Read data from db (dict list formatted).
    :param query: query string
    :return: list
    """
    try:
        with sqlite3.connect(f"./data/{DATABASE}") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(query)
            result: list = cursor.fetchall()
            connection.commit()
    except DatabaseError as e:
        logging.error("Database read data (row) error: ", e)

    return [dict(row) for row in result]
