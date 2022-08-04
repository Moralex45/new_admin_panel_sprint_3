import os
import pathlib

import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv(
    os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(),
        '.env'
        )
    )


class PostgreSettings(BaseSettings):
    database: str = Field('movies_database', env='DB_NAME')
    user: str = Field('app', env='DB_USER')
    password: str = Field('123qwe', env='DB_PASSWORD')
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field(5434, env='DB_PORT')

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


class EsSettings(BaseSettings):
    elastic_protocol: str = Field(..., env='ES_PROTOCOL')
    elastic_host: str = Field(..., env='ES_HOST')
    elastic_port: str = Field(..., env='ES_PORT')

    def get_full_address(self):
        return self.elastic_protocol + '://' + \
            self.elastic_host + ':' + \
            self.elastic_port

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'
