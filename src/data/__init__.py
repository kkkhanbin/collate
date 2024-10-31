from src.config import config
from src.data.db_connection import create_connection

connection = create_connection(config.DB_URL, config.DB_PORT)

__all__ = (
    'create_connection', 'connection'
)
