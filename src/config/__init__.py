import src.config.log  # Простая активация модуля
from .configs import ProductionConfig, BaseConfig, TestingConfig, config
from .utils import default
from .rest import add_resources, RESOURCES

__all__ = (
    'ProductionConfig', 'BaseConfig', 'add_resources',
    'add_tests', 'login_manager', 'log', 'TestingConfig',
    'config'
)
