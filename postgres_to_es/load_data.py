import time
from datetime import datetime

from logzero import logfile, logger

from settings import EsSettings, PostgreSettings
from transformer import Transformer
from pg import PGLoader, create_pg_connect
from esloader import ESLoader
from state import JsonFileStorage, State


logfile("etl.log")


WAIT_SEC = 2

state_key='key'

columns = [
            'id', 'title', 'description', 'imdb_rating',
            'genre', 'director', 'actors_names', 'writers_names',
            'actors', 'writers'
        ]



def etl(db, loader):

    data_transformer = Transformer()
    for row in db.pg_loader():
        data = data_transformer.transform(
            [
                dict(
                    zip(
                        columns, 
                        row
                    )
                )
            ]
        )
        loader.es_load_data(data)
    
    State(
        JsonFileStorage('state.txt')).set_state(
            str(state_key),
            value=str(datetime.now().astimezone())
        )


if __name__ == '__main__':
    logger.info("Start postgres_to_es")
    with create_pg_connect(PostgreSettings().dict()) as pg_conn:
        logger.info("Successful connection to Postgres")

        es_settings = EsSettings()
        address = es_settings.get_full_address()
        loader = ESLoader(address=address)
        logger.info("Successful connection to Elasticsearch")
        loader.create_index('movies')

        db = PGLoader(pg_conn)

        while True:
            etl(db, loader)
            time.sleep(WAIT_SEC)
    