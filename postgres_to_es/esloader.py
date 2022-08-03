import json
from datetime import datetime

from elasticsearch import Elasticsearch
from logzero import logger

from backoff import backoff
from elastic_index import INDEX
from state import JsonFileStorage, State


class ESLoader:
    """
        Загружает данные в Elastic Search
    """
    def __init__(self, address, state_key='key'):
        self.address = address
        self._es = self.connect(address)
        self.data = []
        self.key = state_key

    @backoff()
    def connect(self, address) -> Elasticsearch:
        """
            Вернуть текущее подключение для ES или инициализировать новое
        """
        return Elasticsearch(address)

    @backoff()
    def create_index(self, index: str):
        """
            Создание индекса в ES
        """
        if not self._es.indices.exists(index=index):
            logger.info("Создание индекса - movies")
            self._es.indices.create(index=index, body=INDEX)

    @backoff()
    def bulk_data(self) -> None:
        self._es.bulk(index='movies', body=self.data, refresh=True)

    def load_data(self, query):
        data_json = json.dumps(query)
        load_json = json.loads(data_json)
        for row in load_json:
            for i in row:
                if row[i] is None:
                    row[i] = []
            self.data.append(
                {
                    "create": {"_index": "movies", "_id": row['id']}
                }
            )
            self.data.append(row)
            self.bulk_data()
            self.data.clear()
        State(
            JsonFileStorage('state.txt')).set_state(
                str(self.key),
                value=str(datetime.now().astimezone())
            )
