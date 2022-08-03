import time

from logzero import logfile, logger

from settings import EsSettings, PostgreSettings
from pg import PGLoader, create_pg_connect
from esloader import ESLoader

logfile("etl.log")


WAIT_SEC = 10

columns = [
            'id', 'title', 'description', 'imdb_rating',
            'genre', 'director', 'actors_names', 'writers_names',
            'actors', 'writers'
        ]

batch = 100


def etl(db, loader):

    records = db.pg_loader()
    count_records = len(records)
    index = 0
    block = []
    while count_records != 0:
        if count_records >= batch:
            for row in records[index: index + batch]:
                block.append(dict(zip(columns, row)))
                index += 1
            count_records -= batch
            loader.load_data(block)
            block.clear()
        else:
            loader.load_data(
                [
                    dict(
                        zip(columns, row)
                    ) for row in records[index: index + count_records]
                ]
                )
            count_records -= count_records


if __name__ == '__main__':
    logger.info("Запуск")
    with create_pg_connect(PostgreSettings().dict()) as pg_conn:
        logger.info("Подключение к Postgres успешно")

        es_settings = EsSettings()
        address = es_settings.get_full_address()
        loader = ESLoader(address=address)
        logger.info("Подключение к Elasticsearch успешно")
        loader.create_index('movies')

        db = PGLoader(pg_conn)

        while True:
            etl(db, loader)
            time.sleep(WAIT_SEC)
    