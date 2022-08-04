from elasticsearch import Elasticsearch
from logzero import logger

from backoff import backoff
from elastic_index import INDEX


class ESLoader:
    """
        Загружает данные в Elastic Search
    """
    def __init__(self, address):
        self._es = self.connect(address)
        self.data = []

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
            logger.info("Create index - movies")
            self._es.indices.create(index=index, body=INDEX)

    @backoff()
    def bulk_data(self, data) -> None:
        self._es.bulk(index='movies', body=data, refresh=True)

    def es_load_data(self, query):    

        self.bulk_data(query)
