import config.log  # Простая активация модуля
from .configs import ProductionConfig, BaseConfig, TestingConfig, config
from .jinja import add_tests, TESTS
from .utils import default
from .blueprint import BLUEPRINTS, register_blueprints
from .compare.measurement_units import MEASUREMENT_UNITS
