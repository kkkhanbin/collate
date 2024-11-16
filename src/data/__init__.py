from config import config
from .db_connection import create_connection
from .aicore_connection import AI

connection = create_connection(config.DB_URL, config.DB_PORT)

__all__ = (
    'connection', 'AI'
)
