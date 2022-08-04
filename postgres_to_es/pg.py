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

    def get_state_key(self):
        """
            Получает состояние
        """
        state =State(JsonFileStorage('state.txt')).get_state('key')

        if state is None:
            return datetime.min
        return state

    def pg_loader(self) -> list:
        """
            Загружает данные из PostqreSQL, с использованием
            load_query по batch записей
        """
        self.cursor.execute(load_query % self.get_state_key())
        while batch := self.cursor.fetchmany(self.batch):
            yield from batch
