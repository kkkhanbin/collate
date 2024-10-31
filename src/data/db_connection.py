import os
import logging

from hdbcli import dbapi


def create_connection(url: str, port: int) -> dbapi.Connection:
    if not url or not url.strip():
        raise Exception('Необходимо указать стркоу подключения к базе данных.')

    cc = dbapi.connect(
        address=url,
        port=port,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        encrypt=True
    )

    logging.info(f'Было подключено соединение по адресу {url}:{port}')

    return cc
