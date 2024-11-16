import os
import logging

from hdbcli import dbapi

DB_USER = "DBADMIN"
DB_PASSWORD = "Somepassword11"


def create_connection(url: str, port: int) -> dbapi.Connection:
    if not url or not url.strip():
        raise Exception('Необходимо указать стркоу подключения к базе данных.')

    try:
        cc = dbapi.connect(
            address=url,
            port=port,
            user=DB_USER,
            password=DB_PASSWORD,
            encrypt=True
        )

        return cc

        logging.info(f'Было подключено соединение по адресу {url}:{port}')
    except dbapi.Error as err:
        logging.error(err.errortext)
