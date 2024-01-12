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


def read_data_row(query):
    with sqlite3.connect(f'./data/{DATABASE}') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
    return [dict(row) for row in result]
