from datetime import datetime

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from query import load_query
from backoff import backoff
from state import JsonFileStorage, State


@backoff()
def create_pg_connect(settings: dict) -> _connection:
    """
        Соединение с PostgreSQL
    """
    return psycopg2.connect(**settings, cursor_factory=DictCursor)


class PGLoader:
    """
        Загружает данные из PostgreSQL
    """
    def __init__(self, pg_conn, state_key='key'):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.key = state_key
        self.state_key = State(
                            JsonFileStorage('state.txt')
                            ).get_state(state_key)
        self.batch = 100
        self.data_container = []

    def get_state_key(self):
        """
            Получает состояние
        """
        if self.state_key is None:
            return datetime.min
        return self.state_key

    def pg_loader(self) -> list:
        """
            Загружает данные из PostqreSQL, с использованием
            load_query по batch записей
        """
        self.cursor.execute(load_query % self.get_state_key())
        while True:
            records = self.cursor.fetchmany(self.batch)
            if not records:
                break
            for row in records:
                self.data_container.append(row)
        return self.data_container
