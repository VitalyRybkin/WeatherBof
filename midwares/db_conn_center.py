import sqlite3
import os

from data import config

DATABASE = config.DB


def read_data(query):
    with sqlite3.connect(f'{DATABASE}') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()

    return result


def write_data(query):
    with sqlite3.connect(f'{DATABASE}') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
