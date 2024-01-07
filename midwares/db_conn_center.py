import sqlite3

from data import config

DATABASE = config.DB


def read_data(query):
    with sqlite3.connect(f'./data/{DATABASE}') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()

    return result


def write_data(query):
    with sqlite3.connect(f'./data/{DATABASE}') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
