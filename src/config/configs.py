import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    JSON_AS_ASCII = False
    TRAP_HTTP_EXCEPTIONS = True
    MAX_CONTENT_SIZE = 128 * 1024 * 1024  # 128 мегабайт
    ALLOWED_EXTENSIONS = ()
    FORBIDDEN_EXTENSIONS = (
        'exe'
    )


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    BUNDLE_ERRORS = True


# Здесь можно настраивать текущий конфиг
config = ProductionConfig

__all__ = (
    'BaseConfig', 'ProductionConfig', 'TestingConfig', 'config'
)
