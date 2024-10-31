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
    DB_URL = "50c3870c-b8af-42ea-bf9a-d250c3999d9a.hna2.prod-eu10.hanacloud.ondemand.com"
    DB_PORT = 443


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
